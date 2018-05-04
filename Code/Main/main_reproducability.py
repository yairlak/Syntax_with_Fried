from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses
from scipy import stats
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
contrasts = comparison_list['fields'][2]
union_or_intersection = comparison_list['fields'][6]
comparisons = read_logs_and_comparisons.extract_comparison(contrasts, union_or_intersection, features)

print('Reading log files from experiment...')
log_all_blocks = []
for block in settings.blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, settings, params)
curr_event_ids = set(events[:, 2])
color_curr = dict([item for item in settings.event_colors.items() if item[0] in curr_event_ids])

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
        for band, fmin, fmax in params.iter_freqs:

            event_str = "FIRST_WORD" # "END_WAV_TIMES"]: #""LAST_WORD"]:#  , "KEY"]:
            curr_event_id_to_plot = [s for s in event_ids_epochs if event_str in s] # Filter events

            power, power_ave, baseline = analyses.average_high_gamma(epochs_resampled, curr_event_id_to_plot, band,
                                                                         fmin, fmax, params.freq_step, None, 'trial_wise', params)

            reproducability_matrix = analyses.reproducability(power, power_ave, settings, params)

            file_name = 'reproducability_' + band + '_' + settings.patient + '_channel_' + str(
                settings.channel) + '_micro_Blocks_' + str(
                settings.blocks) + '_Event_id_' + event_str + '_' + settings.channel_name

            # Save to file
            diag = np.diagonal(reproducability_matrix)
            off_diag = reproducability_matrix[np.triu(np.ones(reproducability_matrix.shape, dtype=bool), k=1)]
            tvalue, pvalue = stats.ttest_ind(diag, off_diag)
            with open(os.path.join(settings.path2figures, settings.patient, 'Reproducability', file_name + '.pkl'),
                      'wb') as f:
                pickle.dump([reproducability_matrix, diag, off_diag, tvalue, pvalue], f)

            # Generate and save figure
            from mpl_toolkits.axes_grid1 import make_axes_locatable

            fig, axs = plt.subplots(1, 2, figsize=[30, 20])
            im = axs[0].imshow(reproducability_matrix, vmin=-1, vmax=1)
            axs[0].set_xlabel('Sentence number', fontsize=24)
            axs[0].set_ylabel('Sentence number', fontsize=24)
            divider = make_axes_locatable(axs[0])
            cax = divider.append_axes("right", size="2%", pad=0.1)
            cbar = plt.colorbar(im, cax=cax)
            cbar.ax.set_ylabel('Inter-block Correlation', rotation=270, fontsize=24)
            # cbar = fig.colorbar(cax, ax=axs[0])
            axs[1].hist([diag, off_diag], 20, normed=True,
                        label=['Same sentence (diagonal)', 'Different sentences (off-diagonal)'])
            axs[1].set_xlabel('Inter-block correlation', fontsize=24)
            axs[1].set_ylabel('Normalized counts', fontsize=24)
            axs[1].set_ylim([0, 5])
            axs[1].text(-0.5, 4.2, r'$\mu=$' + "%.2f" % np.mean(diag) + ',\ $\sigma=$' + "%.2f" % np.std(diag), color='b',
                        fontsize=24)
            axs[1].text(-0.5, 4, r'$\mu=$' + "%.2f" % np.mean(off_diag) + ',\ $\sigma=$' + "%.2f" % np.std(off_diag),
                        color='r', fontsize=24)
            axs[1].text(-0.5, 3.8, 'p-value=' + "%.2f" % np.mean(pvalue), color='k', fontsize=24)

            axs[1].legend(loc=1, fontsize=24)
            axs[1].grid(True)
            plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Reproducability', file_name + '.png'))
            print(tvalue, pvalue)

del raw, epochs, epochs_resampled, power, power_ave


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















            # # Calculate average power activity
            # event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
            # power1, power_ave1, P_zero1 = analyses.average_high_gamma(epochs_resampled, event_id_1, band, fmin, fmax,
            #                                                           params.freq_step)
            # event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
            # power2, power_ave2, P_zero2 = analyses.average_high_gamma(epochs_resampled, event_id_2, band, fmin, fmax,
            #                                                           params.freq_step)
            # event_id_3 = [s for s in event_ids_epochs if "LAST_WORD" in s]
            # power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax,
            #                                                     params.freq_step, P_zero1)
            # # event_id_3 = [s for s in event_ids_epochs if "END_WAV" in s]
            # # power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax, params.freq_step, P_zero1)
            #
            # # PLOT
            # file_name = band + '_' + settings.patient + '_micro' + '_Channel_' + str(
            #     settings.channel) + '_Blocks_' + str(settings.blocks) + '_Event_id' + str(
            #     epochs_resampled.event_id.values()) + settings.channel_name + '_lengthSorted_' + str(
            #     preferences.sort_according_to_sentence_length) + '.png'
            # analyses.plot_and_save_average_freq_band(power1, power2, power3, power_ave1, power_ave2, power_ave3, event_id_1,
            #                                          event_id_2, event_id_3, file_name, fig_paradigm, settings,
            #                                          log_all_blocks, preferences)



# cluster16 = raw_spikes.pick_channels(ch_names=[raw_spikes.info['ch_names'][16]])
    # cluster16.plot(start=500, duration=1000)
    # cluster16_data = raw_spikes.get_data(picks=[16])
    # cluster16_data_smoothed = analyses.smooth_with_gaussian(np.squeeze(cluster16_data), gaussian_width=100)
    # plt.plot(raw_spikes.times, cluster16_data_smoothed)
    # plt.xlabel('Time [sec]', fontsize=16)
    # plt.ylabel('Gaussian smoothed spike train', fontsize=16)
    # plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Rasters', 'cluster_16_smoothed_spike_train.png'))
    # plt.close()


# settings.time0 = 1.489760586848367e+15
    # settings.time0 = 25393.747629 # patient 480
    # settings.timeend = settings.timeend + settings.time0

# print('Baseline High-Gamma data, based on first-word alignment')
                # settings.event_types_to_extract = ['FIRST_WORD_TIMES']
                # events_FIRST_WORD_TIMES, _, event_id_FIRST_WORD_TIMES = convert_to_mne.generate_events_array(log_all_blocks, settings, params)
                # epochs_FIRST_WORD_TIMES = mne.Epochs(raw, events_FIRST_WORD_TIMES, event_id_FIRST_WORD_TIMES, params.tmin, params.tmax, baseline=None, preload=True)
                # epochs_FIRST_WORD_TIMES_resampled = epochs_FIRST_WORD_TIMES.copy().resample(params.downsampling_sfreq, npad='auto')
                # event_ids_epochs_FIRST_WORD_TIMES = epochs_FIRST_WORD_TIMES_resampled.event_id.keys()
                # curr_event_id_to_plot = [s for s in event_ids_epochs_FIRST_WORD_TIMES if 'FIRST_WORD_TIMES' in s]
                # _, _, baseline = analyses.average_high_gamma(epochs_FIRST_WORD_TIMES_resampled, curr_event_id_to_plot, 'High-Gamma', 70, 150, params.freq_step, None, params)
