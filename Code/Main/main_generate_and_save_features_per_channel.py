from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
from mne.decoding import GeneralizationAcrossTime
from sklearn.svm import LinearSVC
import sys
import pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
channels_micro = range(1,7,1)
channels_macro = range(1,2,1)


# ------------ START MAIN --------------
print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
# Get (optional) argument from terminal which defines the channel for gamma analysis
if len(sys.argv) > 1:
    print 'Channel ' + sys.argv[1]
    ch = int(sys.argv[1])
    channels_macro = range(ch, ch + 1, 1)
    channels_micro = range(ch, ch + 1, 1)

print('Loading parameters...')
params = load_settings_params.Params()

print('Loading preferences...')
preferences = load_settings_params.Preferences()

print('Loading features and comparisons...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
contrast_names = comparison_list['fields'][1]
contrasts = comparison_list['fields'][2]
align_to = comparison_list['fields'][4]
union_or_intersection = comparison_list['fields'][6]
comparisons = read_logs_and_comparisons.extract_comparison(contrast_names, contrasts, align_to, union_or_intersection, features)
if settings.comparisons is not None: comparisons = [cmp for i, cmp in enumerate(comparisons) if i+1 in settings.comparisons]

print('Reading log files from experiment...')
log_all_blocks = []
for block in settings.blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Loading electrode names for all channels...')
electrode_names = load_data.electrodes_names(settings)

#----- RASTERS ------
if preferences.analyze_micro_single:
    print('Loading spike sorted data (spike clusters)...')
    spikes, settings, electrode_names, electrode_names_from_raw_files, from_channels = load_data.spike_clusters(settings)

    print('Generating MNE raw object for spikes...')
    raw_spikes = convert_to_mne.generate_mne_raw_object_for_spikes(spikes, electrode_names_from_raw_files, settings, params)

    # Draw event times of the paradigm
    fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '_' + str(settings.blocks) + '.png'
    fig_paradigm = mne.viz.plot_events(events_spikes, raw_spikes.info['sfreq'], raw_spikes.first_samp, color=color_curr, event_id=event_id, show=False)
    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
    plt.close(fig_paradigm)

    print('Epoching spiking data...')
    epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, baseline=None, preload=True)
    print(epochs_spikes)

    print('Generate rasters and PSTHs...')
    analyses.generate_rasters(epochs_spikes, log_all_blocks, electrode_names_from_raw_files, from_channels, settings, params, preferences)

# Micro (raw) analysis
if preferences.analyze_micro_raw:
    print("MICRO Channels analysis")
    channels = channels_micro
    for channel in channels:
        settings.channel = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
        print 'Analyzing high-gamma for channel ' + str(channel)
        # Line filter and resample, or load from file
        file_name_epochs = 'micro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(
            channel) + '_line_filtered_resampled-epo'

        # if not settings.load_line_filtered_resampled_epoch_object:
        print('Generating MNE raw object for continuous data...')
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

        print('Line filtering...')
        # raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

        print('Loop over all comparisons: prepare & save data for classification')
        for i, comparison in enumerate(comparisons):
            print('Preparing contrast:' + comparison[2])
            print('Generating event object for MNE from log data...')
            events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, comparison, settings,
                                                                                   params, preferences)
            curr_event_ids = set(events[:, 2])
            color_curr = dict([item for item in settings.event_colors.items() if item[0] in curr_event_ids])

            print('High-Gamma analyses...')
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
            print(epochs)

            print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
            epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
            print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')

            event_ids_epochs = epochs_resampled.event_id.keys()
            for band, fmin, fmax in params.iter_freqs:

                # Parse according to Words
                if any(["WORDS_ON_TIMES" in s for s in event_ids_epochs]):
                    event_str = "WORDS_ON_TIMES"
                    curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s]
                    power, power_ave, _ = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band, fmin, fmax, params.freq_step, False, 'no_baseline', params)

                # Calculate average power activity
                else: # "END_WAV_TIMES"]: #""LAST_WORD"]:#  , "KEY"]:
                    power, power_ave, baseline = analyses.average_high_gamma(epochs_resampled, event_ids_epochs, band,
                                                                                     fmin, fmax, params.freq_step, False, 'no_baseline', params)

                epochs_resampled._data = np.expand_dims(power_ave, axis=1)

                file_name = 'Feature_matrix_' + band + '_' + settings.patient + '_channel_' + str(
                     settings.channel) + '_' + settings.channel_name + '_' + comparison[2] + '_' + comparison[1]

                with open(os.path.join(settings.path2output, settings.patient, 'feature_matrix_for_classification', file_name + '.pkl'), 'wb') as f:
                    pickle.dump([epochs_resampled, comparison, settings, params, preferences] ,f)

                print('Save to: ' + file_name)

    del epochs_resampled, power, power_ave


# MACRO analysis
if preferences.analyze_macro:
    print("MACRO Channels analysis")
    channels = channels_macro

    for channel in channels:
        settings.channel = channel
        settings.channel_macro = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.macro_electrodes(settings)

        print 'Analyzing high-gamma for channel ' + str(channel)
        # Line filter and resample, or load from file
        file_name_epochs = 'macro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(channel) + '_line_filtered_resampled-epo.fif'

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
            epochs_resampled.save(os.path.join(settings.path2epoch_data, file_name_epochs))
        else:
            raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)
            print('Loading already epoch data, after line filtering and resampling: '+ os.path.join(settings.path2epoch_data, file_name_epochs))
            epochs_resampled = mne.read_epochs(os.path.join(settings.path2epoch_data, file_name_epochs))

        fig_paradigm = mne.viz.plot_events(events_spikes, raw.info['sfreq'], raw.first_samp, color=color_curr, event_id=event_id, show=False)
        fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '_' + str(settings.blocks) + '.png'
        plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
        plt.close(fig_paradigm)

        del raw, epochs
        print('High-Gamma analyses...')
        event_ids_epochs = epochs_resampled.event_id.keys()
        for band, fmin, fmax in params.iter_freqs:

            # Parse according to Words
            if any(["WORDS_ON_TIMES" in s for s in event_ids_epochs]):
                event_str = "WORDS_ON_TIMES"
                curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s]
                power, power_ave, _ = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band, fmin,
                                                                  fmax, params.freq_step, False, params)
                file_name = band + '_' + settings.patient + '_channel_' + str(
                    settings.channel) + '_macro_Blocks_' + str(
                    settings.blocks) + '_Event_id_' + event_str + '_' + settings.channel_name + '_lengthSorted_' + str(
                    preferences.sort_according_to_sentence_length) + '_numLettersSorted_' + str(
                    preferences.sort_according_to_num_letters)
                analyses.plot_and_save_high_gamma(power, power_ave, event_str, log_all_blocks, word2pos, file_name,
                                                  settings, params, preferences)

            # Calculate average power activity
            for event_str in ["FIRST_WORD", "LAST_WORD", "KEY"]:
                if any([event_str in s for s in event_ids_epochs]):
                    curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s]
                    if event_str == "FIRST_WORD": # Calculate baseline when alignment is locking to first word.
                        power, power_ave, baseline = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band, fmin, fmax, params.freq_step, None, params)
                    else:
                        if event_str == "KEY":  # Calculate baseline when alignment is locking to first word.
                            power, power_ave, _ = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band, fmin,
                                                                                     fmax, params.freq_step, None, params)
                        else:
                            power, power_ave, _ = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band, fmin, fmax, params.freq_step, baseline, params)

                    file_name = band + '_' + settings.patient + '_channel_' + str(
                        settings.channel) + '_macro_Blocks_' + str(
                        settings.blocks) + '_Event_id_' + event_str + '_' + settings.channel_name
                    if preferences.sort_according_to_sentence_length: file_name = file_name + '_LengthSorted'
                    if preferences.sort_according_to_num_letters: file_name = file_name + '_LengthSorted'
                    file_name = file_name + '.png'
