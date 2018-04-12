from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np
import sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
channels_micro = range(1,2,1)
channels_macro = range(3,60,1)

# ------------ START MAIN --------------

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
# Get (optional) argument from terminal which defines the channel for gamma analysis
if len(sys.argv) > 1:
    print 'Channel ' + sys.argv[1]
    ch = int(sys.argv[1])
    channels_macro = range(ch, ch + 10, 1)

print('Loading parameters...')
params = load_settings_params.Params()

print('Loading preferences...')
preferences = load_settings_params.Preferences()

print('Reading log files from experiment...')
log_all_blocks = []
for block in settings.blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))


# settings.time0 = 1.489760586848367e+15
    # settings.time0 = 25393.747629 # patient 480
    # settings.timeend = settings.timeend + settings.time0

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, settings, params)
color = {1: 'green', 2: 'red', 3: 'blue', 101: 'green', 102: 'red', 103: 'blue', 201: 'green', 202: 'red',
         203: 'blue'}
curr_event_ids = set(events[:, 2])
color_curr = dict([item for item in color.items() if item[0] in curr_event_ids])

print('Loading electrode names for all channels...')
electrode_names = load_data.electrodes_names(settings)

#----- RASTERS ------
if preferences.analyze_micro_single:
    print('Loading spike sorted data (spike clusters)...')
    spikes, settings, electrode_names, electrode_names_from_raw_files, from_channels = load_data.spike_clusters(
        settings)

    print('Generating MNE raw object for spikes...')
    # settings.time0 = 0
    # settings.timeend = 3.159231975000000e+09
    # settings.timeend = 3.313463366666667e+09 # patient 480
    raw_spikes = convert_to_mne.generate_mne_raw_object_for_spikes(spikes, electrode_names_from_raw_files, settings,
                                                                   params)

    # cluster16 = raw_spikes.pick_channels(ch_names=[raw_spikes.info['ch_names'][16]])
    # cluster16.plot(start=500, duration=1000)
    cluster16_data = raw_spikes.get_data(picks=[16])
    cluster16_data_smoothed = analyses.smooth_with_gaussian(np.squeeze(cluster16_data), gaussian_width=100)
    plt.plot(raw_spikes.times, cluster16_data_smoothed)
    plt.xlabel('Time [sec]', fontsize=16)
    plt.ylabel('Gaussian smoothed spike train', fontsize=16)
    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Rasters', 'cluster_16_smoothed_spike_train.png'))
    plt.close()

    # Plot the events to get an idea of the paradigm
    fig_paradigm = mne.viz.plot_events(events_spikes, raw_spikes.info['sfreq'], raw_spikes.first_samp, color=color_curr,
                                       event_id=event_id, show=False)
    fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '_' + str(settings.blocks) + '.png'
    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
    plt.close(fig_paradigm)

    print('Epoching spiking data...')
    epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, baseline=None,
                               preload=True)
    print(epochs_spikes)

    print('Generate rasters and PSTHs...')
    analyses.generate_rasters(epochs_spikes, log_all_blocks, params, settings, preferences)

# MACRO analysis
if preferences.analyze_macro:
    channels = channels_macro

    for channel in channels:
        settings.channel = channel
        settings.channel_macro = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.macro_electrodes(settings)

        print 'Analyzing high-gamma for channel ' + str(channel)
        # Line filter and resample, or load from file
        file_name_epochs = settings.hospital + '_' + settings.patient + '_channel_' + str(channel) + '_line_filtered_resampled-epo.fif'
        if preferences.analyze_micro_raw: file_name_epochs = 'micro_' + file_name_epochs
        if preferences.analyze_macro: file_name_epochs = 'macro_' + file_name_epochs

        if not settings.load_line_filtered_resampled_epoch_object:
            print('Generating MNE raw object for continuous data...')
            raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

            print('Line filtering...')
            # raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

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

        print('High-Gamma analyses...')
        event_ids_epochs = epochs_resampled.event_id.keys()
        for band, fmin, fmax in params.iter_freqs:
            # Calculate average power activity
            event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
            power1, power_ave1, P_zero1 = analyses.average_high_gamma(epochs_resampled, event_id_1, band, fmin, fmax, params.freq_step)
            event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
            power2, power_ave2, P_zero2 = analyses.average_high_gamma(epochs_resampled, event_id_2, band, fmin, fmax, params.freq_step)
            event_id_3 = [s for s in event_ids_epochs if "LAST_WORD" in s]
            power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax, params.freq_step, P_zero1)
            # event_id_3 = [s for s in event_ids_epochs if "END_WAV" in s]
            # power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax, params.freq_step, P_zero1)

            # PLOT
            file_name = band + '_' + settings.patient + '_macro' + '_Channel_' + str(settings.channel) + '_Blocks_' + str(settings.blocks) + '_Event_id' + str(
                epochs_resampled.event_id.values()) + settings.channel_name + '_lengthSorted_' + str(preferences.sort_according_to_sentence_length) + '.png'
            analyses.plot_and_save_average_freq_band(power1, power2, power3, power_ave1, power_ave2, power_ave3, event_id_1, event_id_2, event_id_3, file_name, fig_paradigm, settings, log_all_blocks, preferences)


# Micro (raw) analysis
if preferences.analyze_micro_raw:
    channels = channels_micro
    settings.channel = channel
    print('Loading CSC raw data...')
    raw_CSC_data_in_mat, settings = load_data.raw_in_matlab_format(settings)
    print 'Analyzing high-gamma for channel ' + str(channel)
    # Line filter and resample, or load from file
    file_name_epochs = settings.hospital + '_' + settings.patient + '_channel_' + str(
        channel) + '_line_filtered_resampled-epo.fif'
    if preferences.analyze_micro_raw: file_name_epochs = 'micro_' + file_name_epochs
    if preferences.analyze_macro: file_name_epochs = 'macro_' + file_name_epochs

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
        print(
        'Loading already epoch data, after line filtering and resampling: ' + os.path.join(settings.path2epoch_data,
                                                                                           file_name_epochs))
        epochs_resampled = mne.read_epochs(os.path.join(settings.path2epoch_data, file_name_epochs))

    fig_paradigm = mne.viz.plot_events(events_spikes, raw.info['sfreq'], raw.first_samp, color=color_curr,
                                       event_id=event_id, show=False)
    fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '_' + str(settings.blocks) + '.png'
    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
    plt.close(fig_paradigm)

    print('High-Gamma analyses...')
    event_ids_epochs = epochs_resampled.event_id.keys()
    for band, fmin, fmax in params.iter_freqs:
        # Calculate average power activity
        event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
        power1, power_ave1, P_zero1 = analyses.average_high_gamma(epochs_resampled, event_id_1, band, fmin, fmax,
                                                                  params.freq_step)
        event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
        power2, power_ave2, P_zero2 = analyses.average_high_gamma(epochs_resampled, event_id_2, band, fmin, fmax,
                                                                  params.freq_step)
        event_id_3 = [s for s in event_ids_epochs if "LAST_WORD" in s]
        power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax,
                                                            params.freq_step, P_zero1)
        # event_id_3 = [s for s in event_ids_epochs if "END_WAV" in s]
        # power3, power_ave3, _ = analyses.average_high_gamma(epochs_resampled, event_id_3, band, fmin, fmax, params.freq_step, P_zero1)

        # PLOT
        file_name = band + '_' + settings.patient + '_micro' + '_Channel_' + str(
            settings.channel) + '_Blocks_' + str(settings.blocks) + '_Event_id' + str(
            epochs_resampled.event_id.values()) + settings.channel_name + '_lengthSorted_' + str(
            preferences.sort_according_to_sentence_length) + '.png'
        analyses.plot_and_save_average_freq_band(power1, power2, power3, power_ave1, power_ave2, power_ave3, event_id_1,
                                                 event_id_2, event_id_3, file_name, fig_paradigm, settings,
                                                 log_all_blocks, preferences)

