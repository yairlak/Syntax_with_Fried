from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses
import os, glob
import mne
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import sys
import pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
channels_micro = range(1,89,1)
channels_micro = [1, 2, 18, 46, 59] # 18, 46, 59
channels_macro = range(1,2,1)


# ------------ START MAIN --------------
print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
# Get (optional) argument from terminal which defines the channel for gamma analysis
if len(sys.argv) > 1:
    print('Channel ' + sys.argv[1])
    ch = int(sys.argv[1])
    channels_macro = range(ch, ch + 1, 1)
    channels_micro = range(ch, ch + 1, 1)

print('Loading parameters...')
params = load_settings_params.Params()

print('Loading preferences...')
preferences = load_settings_params.Preferences()

print('Reading log files from experiment...')
log_all_blocks = []
for block in settings.blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, [], word2pos, settings, params, preferences)
curr_event_ids = set(events[:, 2])
color_curr = dict([item for item in settings.event_colors.items() if item[0] in curr_event_ids])

print('Loading electrode names for all channels...')
electrode_names = load_data.electrodes_names(settings)

print("Analyzing channels")
channels = channels_micro
for channel in channels:
    settings.channel = channel
    print('Loading CSC raw data...')
    raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
    print('Analyzing high-gamma for channel ' + str(channel))
    # Line filter and resample, or load from file
    file_name_epochs = settings.hospital + '_' + settings.patient + '_channel_' + str(
        channel) + '_line_filtered_resampled-epo'

    if not settings.load_line_filtered_resampled_epoch_object:
        print('Generating MNE raw object for continuous data...')
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

        print('Line filtering...')
        raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

        print('Epoching data...')

        epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)

        print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
        epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
        print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')

        print('Save Epoch data after line filtering and resampling')
        epochs_resampled.save(os.path.join(settings.path2epoch_data, 'Epochs_' + file_name_epochs + '.fif'))

    else:
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)
        print('Loading epoched data, after line filtering and resampling: ' + os.path.join(settings.path2epoch_data,
                                                                                           file_name_epochs))
        epochs_resampled = mne.read_epochs(os.path.join(settings.path2epoch_data, 'Epochs_' + file_name_epochs + '.fif'))


    del raw
    if not settings.load_line_filtered_resampled_epoch_object: del epochs

    print('High-Gamma analyses...')
    event_ids_epochs = epochs_resampled.event_id.keys()
    # for band, fmin, fmax in params.iter_freqs:
    for band, fmin, fmax in [('High-Gamma', 70, 150)]:

        event_str = "FIRST_WORD" # "END_WAV_TIMES"]: #""LAST_WORD"]:#  , "KEY"]:
        curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s] # Filter events

        power, power_ave, baseline = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band,
                                                                     fmin, fmax, params.freq_step, None, 'trial_wise', params)

        settings.band = band
        settings.event_str = event_str
        analyses.reproducability(power, power_ave, settings, params)

