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
channels = range(48,50)
# channels = [59] # 18, 46, 59
#channels_micro = range(1,130,1)
#channels_micro = [1, 2, 18, 46, 59] # 18, 46, 59
#channels_micro = range(1,89,1)
# channels_micro = [59] # 18, 46, 59
# channels_macro = range(1,2,1)


# ------------ START MAIN --------------
print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
# Get (optional) argument from terminal which defines the channel for gamma analysis
if len(sys.argv) > 1:
    print('Channel ' + sys.argv[1])
    ch = int(sys.argv[1])
    channels = range(ch, ch + 1, 1)
    channels = range(ch, ch + 1, 1)

print('Loading parameters...')
params = load_settings_params.Params()

print('Loading preferences...')
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)

print('Logs: Reading log files from experiment...')
log_all_blocks = []
for block in range(1, 7):
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_comparisons.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, metadata, word2pos, settings, params, preferences)

print('Loading electrode names for all channels...')
electrode_names = load_data.electrodes_names(settings)

print("Analyzing channels")
for channel in channels:
    for blocks in [[1, 3, 5], [2, 4, 6]]:
        print('Channel ' + str(channel) + ', blocks: ' + str(blocks))
        settings.channel = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
        print('Analyzing high-gamma for channel ' + str(channel))
        # Line filter and resample, or load from file
        file_name_epochs = settings.hospital + '_' + settings.patient + '_channel_' + str(
            channel) + '_line_filtered_resampled-epo'

        print('Generating MNE raw object for continuous data...')
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)
        del raw_CSC_data_in_mat

        print('Line filtering...')
        raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

        print('Epoching data...')
        if preferences.use_metadata_only:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None,
                                preload=True)
        else:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)
        del raw

        print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
        epochs.resample(params.downsampling_sfreq, npad='auto')
        print('New sampling rate:', epochs.info['sfreq'], 'Hz')


        print('High-Gamma analyses...')
        # event_ids_epochs = epochs.event_id.keys()
        # for band, fmin, fmax in params.iter_freqs:
        for band, fmin, fmax in [('High-Gamma', 70, 150)]:

            # event_str = "FIRST_WORD" # "END_WAV_TIMES"]: #""LAST_WORD"]:#  , "KEY"]:
            # curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s] # Filter events
            str_blocks = ['block == {} or '.format(block) for block in blocks]
            str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
            query = 'All_trials == 1 and word_position == 1 and ' + str_blocks
            power, power_ave, baseline = analyses.average_high_gamma(epochs[query], band, fmin, fmax, params.freq_step, None, 'trial_wise', params)

            power.metadata = epochs[query].metadata
            settings.band = band
            # settings.event_str = event_str
            settings.blocks = blocks
            analyses.reproducability(power, power_ave, log_all_blocks, settings, params)

