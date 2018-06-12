from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
channels = range(49,57)


# --------- Read params from outside --------
# Get (optional) argument from terminal which defines the channel for gamma analysis
if len(sys.argv) > 1:
    print 'Channel ' + sys.argv[1]
    ch = int(sys.argv[1])
    channels = range(ch, ch + 1, 1)

# ------------ START MAIN --------------
print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

# --------------------------------------
# if preferences.run_contrasts or preferences.use_metadata_only:
print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
contrast_names = comparison_list['fields'][1][settings.comparisons]
contrasts = comparison_list['fields'][2][settings.comparisons]
cond_labels = comparison_list['fields'][3][settings.comparisons]
cond_labels = [cond_label[1:-1].split(',') for cond_label in cond_labels]
align_to = comparison_list['fields'][4][settings.comparisons]
blocks = comparison_list['fields'][5][settings.comparisons]
sortings = comparison_list['fields'][6][settings.comparisons]
sortings = [s.split(',') if isinstance(s, unicode) else [] for s in sortings]
union_or_intersection = comparison_list['fields'][7][settings.comparisons]
comparisons = read_logs_and_comparisons.extract_comparison(contrast_names, contrasts, align_to, blocks, union_or_intersection, features, preferences)

# --------------------------------------------
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

#----- RASTERS ------
if preferences.analyze_micro_single:
    print('Loading spike sorted data (spike clusters)...')
    spikes, settings, electrode_names_from_raw_files, from_channels = load_data.spike_clusters(settings)

    print('Generating MNE raw object for spikes...')
    raw_spikes = convert_to_mne.generate_mne_raw_object_for_spikes(spikes, electrode_names_from_raw_files, settings, params)

    # Draw event times of the paradigm
    fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '.png'
    fig_paradigm = mne.viz.plot_events(events_spikes, raw_spikes.info['sfreq'], raw_spikes.first_samp, event_id=event_id, show=False)
    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
    plt.close(fig_paradigm)

    print('Epoching spiking data...')
    epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None, preload=True)
    print(epochs_spikes)

    # event_ids_epochs = epochs_spikes.event_id.keys()
    # for event_str in ["FIRST_WORD", "LAST_WORD", "END_WAV_TIMES"]:  # "END_WAV_TIMES"]: #""LAST_WORD"]:#  , "KEY"]:
    #     if any([event_str in s for s in event_ids_epochs]):
    #         curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s]
    print('Generate rasters and PSTHs...')
    # settings.events_to_plot = curr_event_id_to_plot
    if preferences.use_metadata_only:
        for contrast_name, comparison, curr_blocks, curr_align_to, curr_sorting, cond_label in zip(contrast_names,
                                                                                                   comparisons, blocks,
                                                                                                   align_to, sortings,
                                                                                                   cond_labels):
            preferences.sort_according_to_key = [s.strip().encode('ascii') for s in curr_sorting]
            str_blocks = ['block == {} or '.format(block) for block in eval(curr_blocks)]
            str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
            if curr_align_to == 'FIRST':
                str_align = 'word_position == 1'
            elif curr_align_to == 'LAST':
                str_align = 'word_position == sentence_length'
            elif curr_align_to == 'END':
                str_align = 'word_position == -1'
            elif curr_align_to == 'EACH':
                str_align = 'word_position > 0'

            for query_cond, label_cond in zip(comparison, cond_label):
                # file_name = str(settings.patient + '_channel_' + str(settings.channel) + '_Blocks_'
                #                 + curr_blocks + '_' + label_cond + '_' + curr_align_to + '_' + settings.channel_name)
                # for key_sort in preferences.sort_according_to_key:
                #     file_name += '_' + key_sort + 'Sorted'

                # IX1 = settings.channel_name.find('_0019')
                # if IX1 == -1:
                #     IX1 = settings.channel_name.find('.ncs')
                # probe_name = settings.channel_name[0:IX1 - 1]
                # if (not os.path.isfile(os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name,
                #                                     file_name + '.png'))) or settings.overwrite_existing_output_files:
                query = query_cond + ' and ' + str_align + ' and ' + str_blocks

                analyses.generate_rasters(epochs_spikes[query], query, electrode_names_from_raw_files, from_channels, settings, params, preferences)

# Electrodes (Time-frequency analysis)
if preferences.analyze_micro_raw:
    print("Time-frequency analysis of all channels")
    for channel in channels:
        settings.channel = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
        print 'Analyzing high-gamma for channel ' + str(channel)
        # Line filter and resample, or load from file
        file_name_epochs = 'micro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(
            channel) + '_line_filtered_resampled-epo'

        print('Generating MNE raw object for continuous data...')
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

        print('Line filtering...')
        raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

        print('Epoching data...')
        if preferences.use_metadata_only:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None, preload=True)
        else:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)

        print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
        epochs.resample(params.downsampling_sfreq, npad='auto')
        print('New sampling rate:', epochs.info['sfreq'], 'Hz')

        print('Plot paradigm')
        fig_paradigm = mne.viz.plot_events(events_spikes, raw.info['sfreq'], raw.first_samp,
                                           event_id=event_id, show=False)
        fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '.png'
        plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
        plt.close(fig_paradigm)

        del raw, raw_CSC_data_in_mat

        print('Time-frequency analyses...')
        event_ids_epochs = epochs.event_id.keys()
        for band, fmin, fmax in params.iter_freqs:
            print('Band: ' + band)

            if preferences.use_metadata_only:
                for contrast_name, comparison, curr_blocks, curr_align_to, curr_sorting, cond_label in zip(contrast_names, comparisons, blocks, align_to, sortings, cond_labels):
                    preferences.sort_according_to_key = [s.strip().encode('ascii') for s in curr_sorting]
                    str_blocks = ['block == {} or '.format(block) for block in eval(curr_blocks)]
                    str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
                    if curr_align_to == 'FIRST':
                        str_align = 'word_position == 1'
                    elif curr_align_to == 'LAST':
                        str_align = 'word_position == sentence_length'
                    elif curr_align_to == 'END':
                        str_align = 'word_position == -1'
                    elif curr_align_to == 'EACH':
                        str_align = 'word_position > 0'

                    for query_cond, label_cond in zip(comparison, cond_label):
                        file_name = str(band + '_' + settings.patient + '_channel_' + str(settings.channel) + '_Blocks_'
                                        + curr_blocks + '_' + label_cond + '_' + curr_align_to + '_' + settings.channel_name)
                        for key_sort in preferences.sort_according_to_key:
                            file_name += '_' + key_sort + 'Sorted'

                        IX1 = settings.channel_name.find('_0019')
                        if IX1 == -1:
                            IX1 = settings.channel_name.find('.ncs')
                        probe_name = settings.channel_name[0:IX1 - 1]
                        if (not os.path.isfile(os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name,
                                                           file_name + '.png'))) or settings.overwrite_existing_output_files:

                            query_baseline = query_cond + ' and word_position == 1 and ' + str_blocks
                            _, _, baseline = analyses.average_high_gamma(epochs[query_baseline], band,
                                                                                         fmin, fmax, params.freq_step, None,
                                                                                         'trial_wise', params)

                            query = query_cond + ' and ' + str_align + ' and ' + str_blocks
                            if not curr_align_to == 'EACH':
                                power, power_ave, _ = analyses.average_high_gamma(epochs[query],
                                                                                      band,
                                                                                      fmin, fmax, params.freq_step, baseline,
                                                                                      'trial_wise', params)
                            else:
                                power, power_ave, _ = analyses.average_high_gamma(epochs[query],
                                                                                  band,
                                                                                  fmin, fmax, params.freq_step,
                                                                                  [],
                                                                                  'no_baseline', params)


                            power.tmin = epochs.tmin; power.tmax = epochs.tmax; power.metadata = epochs[query].metadata
                            analyses.plot_and_save_high_gamma(power, power_ave, curr_align_to, eval(curr_blocks), probe_name, file_name,
                                                              settings, params, preferences)
                        else:
                            print('File already exists')