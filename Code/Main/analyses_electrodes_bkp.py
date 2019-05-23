from __future__ import division
import numpy as np
import os
import mne
import matplotlib.pyplot as plt
import pickle
from operator import itemgetter
from functions import load_data, convert_to_mne
from functions.auxilary_functions import smooth_with_gaussian
from functions.auxilary_functions import get_queries


def generate_time_freq_plots(channels, events, event_id, metadata, comparisons, settings, params, preferences):
    print("Time-frequency analysis of all channels")
    for channel in channels:
        settings.channel = channel
        print('Loading CSC raw data...')
        raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
        print('Analyzing high-gamma for channel ' + str(channel))
        # Line filter and resample, or load from file
        file_name_epochs = 'micro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(
            channel) + '_line_filtered_resampled-epo'

        print('Generating MNE raw object for continuous data...')
        raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

        if channel>0: # if not microphone
            print('Line filtering...')
            raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

        print('Epoching data...')
        if preferences.use_metadata_only:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None,
                                preload=True)
        else:
            epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)

        if channel>0:
            print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
            epochs.resample(params.downsampling_sfreq, npad='auto')
            print('New sampling rate:', epochs.info['sfreq'], 'Hz')

            del raw, raw_CSC_data_in_mat

            print('Time-frequency analyses...')
            for band, fmin, fmax in params.iter_freqs:
                print('Band: ' + band)

                if preferences.use_metadata_only:
                    for i, comparison in enumerate(comparisons):
                        print('Contrast: ' + comparison['contrast_name'])
                        # queries = get_queries(comparison)
                        preferences.sort_according_to_key = [s.strip() for s in comparison['sorting']]
                        print(preferences.sort_according_to_key)
                        str_blocks = ['block == {} or '.format(block) for block in eval(comparison['blocks'])]
                        str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
                        if comparison['align_to'] == 'FIRST':
                            str_align = 'word_position == 1'
                        elif comparison['align_to'] == 'LAST':
                            str_align = 'word_position == sentence_length'
                        elif comparison['align_to'] == 'END':
                            str_align = 'word_position == -1'
                        elif comparison['align_to'] == 'EACH':
                            str_align = 'word_position > 0'

                        for query_cond, label_cond in zip(comparison['query'], comparison['cond_labels']):
                            # If part-of-sppech (pos) is found in query then add double quotes (") around value, e.g. (pos==VB --> pos =="VB"). Otherwise pandas expects a variable.
                            new_query_cond = ''
                            i = 0
                            while i < len(query_cond):
                                if query_cond[i:i + len('pos==')] == 'pos==':
                                    reminder = query_cond[i + len('pos==')::]
                                    temp_list = reminder.split(" ", 1)
                                    new_query_cond = new_query_cond + 'pos=="' + temp_list[0] + '" '
                                    i = i + 6 + len(temp_list[0])
                                else:
                                    new_query_cond += query_cond[i]
                                    i += 1
                            query_cond = new_query_cond

                            file_name_root = band + '_' + settings.patient + '_Blocks_' + comparison['blocks'] + '_' + label_cond + '_' + comparison['align_to']
                            file_name = file_name_root + '_' + '_channel_' + str(settings.channel) + settings.channel_name

                            for key_sort in preferences.sort_according_to_key:
                                file_name += '_' + key_sort + 'Sorted'

                            if settings.patient == 'patient_493':
                                find_str = '_0016'
                            else:
                                find_str = '_0019'
                            IX1 = settings.channel_name.find(find_str)
                            if IX1 == -1:
                                IX1 = settings.channel_name.find('.ncs')
                            probe_name = settings.channel_name[0:IX1 - 1]
                           
                            with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name_root + '.txt'), 'w') as f:
                                stimuli_of_curr_query = list(set(list(metadata.query(query_cond)['sentence_string'])))
                                stimuli_of_curr_query = [l+'\n' for l in stimuli_of_curr_query]
                                f.writelines(stimuli_of_curr_query)

                            if (not os.path.isfile(
                                    os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name,
                                                 file_name + '.png'))) or settings.overwrite_existing_output_files:

                                query_baseline = query_cond + ' and word_position == 1 and ' + str_blocks
                                _, _, baseline = average_high_gamma(epochs[query_baseline], band,
                                                                             fmin, fmax, params.freq_step, None,
                                                                             'trial_wise', params)

                                query = query_cond + ' and ' + str_align + ' and ' + str_blocks
                                if not comparison['align_to'] == 'EACH':
                                    power, power_ave, _ = average_high_gamma(epochs[query],
                                                                                      band,
                                                                                      fmin, fmax, params.freq_step,
                                                                                      baseline,
                                                                                      'trial_wise', params)
                                else:
                                    power, power_ave, _ = average_high_gamma(epochs[query],
                                                                                      band,
                                                                                      fmin, fmax, params.freq_step,
                                                                                      [],
                                                                                      'no_baseline', params)

                                if preferences.save_features_for_classification:
                                    epochs_power = epochs[query].copy()
                                    epochs_power.times = power.times
                                    epochs_power._data = power_ave
                                    epochs_power.metadata = epochs[query].metadata


                                    plot_and_save_high_gamma(epochs_power, comparison['align_to'], eval(comparison['blocks']),
                                                                      probe_name, file_name,
                                                                      settings, params, preferences)
                                    epochs_power._data = np.expand_dims(power_ave, axis=1) # To be compatible with MNE functions: add a middle singelton dimenstion for number of channels
                                    file_name = 'Feature_matrix_' + band + '_' + settings.patient + '_channel_' + str(
                                            settings.channel) + '_' + query

                                    with open(os.path.join(settings.path2output, settings.patient,
                                                           'feature_matrix_for_classification', file_name + '.pkl'), 'wb') as f:
                                        pickle.dump([epochs_power, query, settings, params, preferences], f)

                                    print('Save to: ' + file_name)
                            else:
                                print('File already exists')
        elif channel==0:
            fmin_mic = 300 # vowel freuqency band
            fmax_mic = 1400 # vowel freuqency band
            fmic_freq_step = 500 # vowel freuqency band
            band = 'Speech'
            print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
            epochs.resample(3000, npad='auto')
            print('New sampling rate:', epochs.info['sfreq'], 'Hz')

            del raw, raw_CSC_data_in_mat
            if preferences.use_metadata_only:
                for i, comparison in enumerate(comparisons):
                    print('Contrast: ' + comparison['contrast_name'])
                    # queries = get_queries(comparison)
                    preferences.sort_according_to_key = [str(s.strip().encode('ascii')) for s in comparison['sorting']]
                    print(preferences.sort_according_to_key)
                    print('Sorting: ' + '_'.join(preferences.sort_according_to_key))
                    str_blocks = ['block == {} or '.format(block) for block in eval(comparison['blocks'])]
                    str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
                    if comparison['align_to'] == 'FIRST':
                        str_align = 'word_position == 1'
                    elif comparison['align_to'] == 'LAST':
                        str_align = 'word_position == sentence_length'
                    elif comparison['align_to'] == 'END':
                        str_align = 'word_position == -1'
                    elif comparison['align_to'] == 'EACH':
                        str_align = 'word_position > 0'

                    for query_cond, label_cond in zip(comparison['query'], comparison['cond_labels']):
                        file_name_root = band + '_' + settings.patient + '_channel_'+ str(settings.channel) + '_Blocks_' + comparison['blocks'] + '_' + label_cond + '_' + comparison['align_to']
                        file_name = file_name_root + '_' + settings.channel_name

                        for key_sort in preferences.sort_according_to_key:
                            file_name += '_' + key_sort + 'Sorted'

                        if settings.patient == 'patient_479':
                            IX1 = settings.channel_name.find('_0019')
                        elif settings.patient == 'patient_493':
                            IX1 = settings.channel_name.find('_0016')
                        else:
                            IX1 = settings.channel_name.find('.ncs')
                        probe_name = settings.channel_name[0:IX1 - 1]

                        os.makedirs(os.path.join(settings.path2output, settings.patient, 'HighGamma'), exist_ok=True)
                        with open(os.path.join(settings.path2output, settings.patient, 'HighGamma',
                                               file_name_root + '.txt'), 'w') as f:
                            stimuli_of_curr_query = list(set(list(metadata.query(query_cond)['sentence_string'])))
                            stimuli_of_curr_query = [l + '\n' for l in stimuli_of_curr_query]
                            f.writelines(stimuli_of_curr_query)

                        if (not os.path.isfile(
                                os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name,
                                             file_name + '.png'))) or settings.overwrite_existing_output_files:

                            query_baseline = query_cond + ' and word_position == 1 and ' + str_blocks
                            _, _, baseline = average_high_gamma(epochs[query_baseline], band,
                                                                fmin_mic, fmax_mic, fmic_freq_step, None,
                                                                'trial_wise', params)

                            query = query_cond + ' and ' + str_align + ' and ' + str_blocks

                            power, power_ave, _ = average_high_gamma(epochs[query],
                                                                     band,
                                                                     fmin_mic, fmax_mic, fmic_freq_step,
                                                                     baseline,
                                                                     'trial_wise', params)

                            # power, power_ave, _ = average_high_gamma(epochs[query],
                            #                                              band,
                            #                                              fmin_mic, fmax_mic, fmic_freq_step,
                            #                                              [],
                            #                                              'no_baseline', params)
                            epochs_power = epochs[query].copy()
                            epochs_power.times = power.times
                            epochs_power._data = power_ave
                            epochs_power.metadata = epochs[query].metadata

                            plot_and_save_high_gamma(epochs_power, comparison['align_to'], eval(comparison['blocks']),
                                                     probe_name, file_name,
                                                     settings, params, preferences)
                            # mic = epochs[query].get_data()
                            # mic = np.squeeze(mic)
                            # mic2 = np.power(mic, 2)
                            #
                            # epochs_mic = epochs[query].copy()
                            # epochs_mic._data = mic2
                            # epochs_mic.metadata = epochs[query].metadata
                            #
                            # plot_and_save_high_gamma(epochs_mic, comparison['align_to'], eval(comparison['blocks']),
                            #                          probe_name, file_name,
                            #                          settings, params, preferences)
                            # mic_rms = []
                            # window = np.ones(10) / float(10)
                            # for rw in range(mic2.shape[0]):
                            #     vec = np.sqrt(np.convolve(mic2[rw, :], window, 'valid'))
                            #     mic_rms[rw, :] = vec
                            # print(mic_rms.shape)

                        else:
                            print('File already exists')

def average_high_gamma(epochs, band, fmin, fmax, fstep, baseline, baseline_type, params):
    freqs = np.arange(fmin, fmax, fstep)
    # -------------------------------
    # - delta_F =  2 * F / n_cycles -
    # - delta_T = n_cycles / F / pi -
    # - delta_T * delta_F = 2 / pi  -
    # -------------------------------
    # n_cycles = freq[0] / freqs * 3.14
    # n_cycles = freqs / 2.

    if band == 'High-Gamma':
        n_cycles = 20
    elif band == 'Speech':
        n_cycles = 7
    else:
        n_cycles = 7  # Fieldtrip's default


    power = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, n_jobs=-2, average=False, n_cycles=n_cycles,
                                          return_itc=False, picks=[0])
    power_ave = np.squeeze(np.average(power.data, axis=2))
    # Baseline data
    if baseline is None:
        IX = (epochs.times > -abs(params.baseline_period / 1e3)) & (epochs.times < 0) # indices to relevant times
        if baseline_type == 'subtract_average':
            baseline = np.mean(power_ave[:, IX]) # For baseline: Average over negative times (assuming first word alignment)
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
        elif baseline_type == 'trial_wise':
            baseline = np.mean(power_ave[:, IX], axis=1) # For baseline: Average over negative times (assuming first word alignment)
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])

    else:
        if baseline_type == 'subtract_average':
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
            print("Baseline: subtract average")
        elif baseline_type == 'trial_wise':
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])
            print("Baseline: trial-wise")
        elif baseline_type == 'no_baseline':
            power_ave_baselined = 10 * np.log10(power_ave)  # don't apply any baseline

    # Gaussian smooth of time-freq results if chosen:
    if params.smooth_time_freq > 0:
        power_ave_baselined_smoothed = np.empty(power_ave_baselined.shape)
        for i in range(power_ave_baselined.shape[0]):
            power_ave_baselined_smoothed[i, :] = smooth_with_gaussian(power_ave_baselined[i, :], params.smooth_time_freq)
    else:
        power_ave_baselined_smoothed = power_ave_baselined

    return power, power_ave_baselined_smoothed, baseline


def plot_and_save_high_gamma(epochs_power, align_to, blocks, probe_name, file_name, settings, params, preferences):
    from scipy import stats
    from sklearn import linear_model
    from sklearn.metrics import r2_score

    # Remove 0.2 sec from each side due to boundary effects
    IX_smaller_time_window = (epochs_power.times > epochs_power.tmin + 0.2) & (epochs_power.times < epochs_power.tmax - 0.2)  # relevant times
    power_ave = epochs_power._data[:, IX_smaller_time_window]
    power_ave_zscore = stats.zscore(power_ave)
    power_ave[(power_ave_zscore > 3) | (power_ave_zscore < -3)] = np.NaN

    # Sort if needed
    if preferences.sort_according_to_key:
        fields_for_sorting = []
        for field in preferences.sort_according_to_key:
            fields_for_sorting.append(epochs_power.metadata[field])
        if len(fields_for_sorting) == 1:
            mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])),fields_for_sorting[0])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
            mylist_sorted = sorted(mylist, key=itemgetter(1))
        elif len(fields_for_sorting) == 2:
            mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                               fields_for_sorting[1])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
            mylist_sorted = sorted(mylist, key=itemgetter(1, 2))
        power_ave = power_ave[IX, :]

    # Indices for special time window for analysis (e.g., 200-500ms after end of sentence)
    IX = (epochs_power.times > params.window_st / 1e3) & (epochs_power.times < params.window_ed / 1e3)

    # Run a linear regression if sorted according to, e.g., sentence length
    r2_string = 'No regression calc'
    if preferences.sort_according_to_key:
        X = np.asarray([tup[1] for tup in mylist_sorted])
        y = np.nanmean(power_ave[:, IX], axis=1)  # mean activity in params.window_st-ed.
        IX_nan = np.isnan(y)
        X = X[~IX_nan]; y = y[~IX_nan]
        regr = linear_model.LinearRegression()
        regr.fit(np.expand_dims(X, 1), y)
        y_pred = regr.predict(np.expand_dims(X, 1))
        r2 = r2_score(y, y_pred)
        r2_string = '%s $ R^2=%1.2f$' % (preferences.sort_according_to_key[0], r2)

    # Plot
    fig = plt.figure(figsize=(20, 12))
    ax0 = plt.subplot2grid((12, 13), (0, 0), rowspan=10, colspan=10)
    ax1 = plt.subplot2grid((12, 13), (0, 10), rowspan=10, colspan=2)
    ax2 = plt.subplot2grid((12, 13), (10, 0), rowspan=2, colspan=10)
    cbaxes = plt.subplot2grid((12, 13), (0, 12), rowspan=10)

    vmax1 = np.nanpercentile(power_ave, 95)
    vmin1 = np.nanpercentile(power_ave, 5)
    map = ax0.imshow(power_ave,
                     extent=[np.min(epochs_power.times)+0.2, np.max(epochs_power.times)-0.2, 1, epochs_power._data.shape[0] + 1],
                     interpolation='nearest',
                     aspect='auto', vmin=vmin1, vmax=vmax1, cmap='jet')
    cbar = plt.colorbar(map, cax=cbaxes)
    cbar.set_label(label='Power (dB)', size=22)

    ax0.set_ylabel('Trial', fontsize=24)
    ax0.tick_params(axis='x', which='both', bottom='off', labelbottom='off')

    if preferences.sort_according_to_key:
        ax0.set_yticks(range(0, len(fields_for_sorting[0]), preferences.step))
        yticklabels = np.sort(fields_for_sorting[0])[::preferences.step]
        yticklabels = yticklabels[::-1]
        ax0.set_yticklabels(yticklabels)
        plt.setp(ax0, ylabel=preferences.sort_according_to_key[0])

    ax1.plot(np.nanmean(power_ave[:, IX], axis=1), np.arange(1, 1 + power_ave.shape[0]))
    ax1.set_xlabel('Mean activity\n' + r2_string)
    ax1.set_ylim([1, 1 + power_ave.shape[0]])
    ax1.set_xlim([0, np.nanmean(power_ave) + 3*np.nanstd(power_ave)])
    ax1.tick_params(axis='y', which='both', left='off', labelleft='off', direction='in')


    IX_smaller_time_window = (epochs_power.times > min(epochs_power.times) + 0.2) & (epochs_power.times < max(epochs_power.times) - 0.2)  # indices to relevant times
    ax2.plot(epochs_power.times[IX_smaller_time_window], stats.zscore(np.nanmean(power_ave, axis=0)))
    ax2.set_xlabel('Time [sec]', fontsize=24)
    ax2.set_ylabel('Mean activity (zscore)', fontsize=18)
    ax2.set_xlim([np.min(epochs_power.times)+0.2, np.max(epochs_power.times)-0.2])
    ax2.axhline(y=3, linestyle='--', linewidth=3, color='g')
    ax2.axhline(y=-3, linestyle='--', linewidth=3, color='g')
    ax2.set_ylim([-6, 6])

    # Add vertical lines
    ax0.axvline(x=0, linestyle='--', linewidth=3, color='k')
    ax2.axvline(x=0, linestyle='--', linewidth=3, color='k')
    if align_to == "FIRST" and (set(blocks) & set([1,3,5])):
        ax0.axvline(x=params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
    elif align_to == "LAST" and (set(blocks) & set([1,3,5])):
        ax0.axvline(x=-params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=-2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=-3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
    elif align_to == "END" and (set(blocks) & set([1,3,5])):
        ax0.axvline(x= -params.word_ON_duration * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x= (-params.SOA - params.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x= (-2*params.SOA - params.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x= -params.word_ON_duration * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x= (-params.SOA - params.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x= (-2*params.SOA - params.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')

    print('Saving as - ' + os.path.join(settings.path2figures, settings.patient, 'HighGamma', file_name + '.png'))
    if not os.path.exists(os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name)):
        os.makedirs(os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name))
    fig.savefig(os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name, file_name + '.png'))
    plt.close(fig)


def reproducability(power, power_ave, log_all_blocks, settings, params):
    from scipy import stats
    from operator import itemgetter
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    sort_according_to_key = ['block', 'sentence_number', 'sentence_length']
    fields_for_sorting = []
    for field in sort_according_to_key:
        fields_for_sorting.append(power.metadata[field])
    mylist = [(i, j, k, l) for (i, j, k, l) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0], fields_for_sorting[1], fields_for_sorting[2])]
    IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
    lengths = [i[3] for i in sorted(mylist, key=itemgetter(1, 2))]
    power_ave = power_ave[IX, :]

    # Assumes trials are in chronolgical order, and block size is 152
    num_trials_in_block = 152
    time_st = 0
    time_ed = 1.5 # [sec]
    IX_timewindow = (power.times > time_st) & (power.times < time_ed)

    power_ave_blocks = []
    for block in range(len(settings.blocks)):
        # IX_trials_curr_block = log_all_blocks[block].SENTENCE_NUM_ORDER
        # IX_trials_curr_block = [i-1 for i in IX_trials_curr_block]
        st = block * 152
        ed = (block + 1) * 152
        curr_block_power = power_ave[st:ed, IX_timewindow]
        curr_lengths = lengths[st:ed]
        mylist = [(i, j) for (i, j) in zip(range(len(curr_lengths)), curr_lengths)]
        IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]

        power_ave_blocks.append(curr_block_power[IX, :])
    # power_ave_sorted = np.vstack(power_ave_blocks)

    reproducability_matrix = np.zeros([num_trials_in_block, num_trials_in_block])
    for trial_i in range(num_trials_in_block):
        for trial_j in range(trial_i, num_trials_in_block, 1):
            vec_i = power_ave_blocks[0][trial_i, :] # First block
            vec1_j = power_ave_blocks[1][trial_j, :] # Second block
            vec2_j = power_ave_blocks[2][trial_j, :] # Third block

            rho = np.mean([np.corrcoef(vec_i, vec1_j)[0, 1], np.corrcoef(vec_i, vec2_j)[0, 1]])
            reproducability_matrix[trial_i, trial_j] = rho

    file_name = 'reproducability_' + settings.band + '_' + settings.patient + '_channel_' + str(
        settings.channel) + '_Blocks_' + str(
        settings.blocks) + '_Event_id_FIRST_WORD_' + settings.channel_name

    # Save to file
    diag = np.diagonal(reproducability_matrix)
    off_diag = reproducability_matrix[np.triu(np.ones(reproducability_matrix.shape, dtype=bool), k=1)]
    tvalue, pvalue = stats.ttest_ind(diag, off_diag)
    D, pvalue = stats.ks_2samp(diag, off_diag)
    with open(os.path.join(settings.path2figures, settings.patient, 'Reproducability', file_name + '.pkl'),
              'wb') as f:
        pickle.dump([reproducability_matrix, diag, off_diag, tvalue, pvalue], f)

    fig, axs = plt.subplots(2, 3, figsize=[30, 20])
    im = axs[0, 0].imshow(reproducability_matrix, vmin=-1, vmax=1)
    axs[0, 0].set_xlabel('Sentence length', fontsize=24)
    axs[0, 0].set_ylabel('Sentence length', fontsize=24)
    step = 10
    plt.setp(axs[0, 0],
             xticks = range(0, len(curr_lengths), step),
             xticklabels=[str(n) for n in np.asarray(curr_lengths)[IX][0::step]],
             yticks=range(0, len(curr_lengths), step),
             yticklabels=[str(n) for n in np.asarray(curr_lengths)[IX][0::step]])
    divider = make_axes_locatable(axs[0, 0])
    cax = divider.append_axes("right", size="2%", pad=0.1)
    cbar = plt.colorbar(im, cax=cax)
    cbar.ax.set_ylabel('Inter-block Correlation', rotation=270, fontsize=24, labelpad=25)
    # cbar = fig.colorbar(cax, ax=axs[0])
    axs[0, 1].hist([diag, off_diag], 20, normed=True,
                label=['Same sentence', 'Different sentences'])
    axs[0, 1].set_xlabel('Inter-block correlation', fontsize=24)
    axs[0, 1].set_ylabel('Normalized counts', fontsize=24)
    axs[0, 1].set_ylim([0, 5])
    axs[0, 1].set_xlim([-1, 1])
    axs[0, 1].text(-0.9, 4.6, r'$\mu=$' + "%.2f" % np.mean(diag) + ',\ $\sigma=$' + "%.2f" % np.std(diag), color='b',
                fontsize=24)
    axs[0, 1].text(-0.9, 4.3, r'$\mu=$' + "%.2f" % np.mean(off_diag) + ',\ $\sigma=$' + "%.2f" % np.std(off_diag),
                color='g', fontsize=24)
    axs[0, 1].text(-0.9, 3.8, 'KS, p-value=' + "%.4f" % np.mean(pvalue), color='k', fontsize=24)
    axs[0, 1].text(-0.9, 3.5, 'KS, D=' + "%.4f" % np.mean(D), color='k', fontsize=24)

    axs[0, 1].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0, fontsize=16)
    axs[0, 1].grid(True)
    print(tvalue, pvalue)

    # all_blocks = []
    # for block in range(3):
    #     vec_all_trials = []
    #     for trial_i in range(num_trials_in_block):
    #         vec_all_trials.append(power_ave[trial_i + block*num_trials_in_block, IX_timewindow])
    #     all_blocks.append(vec_all_trials)

    actual_mean_rho = np.mean([np.corrcoef(np.hstack(power_ave_blocks[0]), np.hstack(power_ave_blocks[1]))[0, 1],
             np.corrcoef(np.hstack(power_ave_blocks[0]), np.hstack(power_ave_blocks[2]))[0, 1]])

    import random
    random.seed(1)
    num_perumtations = 1000
    mean_rho = []
    for perm in range(num_perumtations):
        shuffled_trials_block_1 = random.sample(power_ave_blocks[0], len(power_ave_blocks[0]))
        mean_rho.append(np.mean([np.corrcoef(np.hstack(shuffled_trials_block_1), np.hstack(power_ave_blocks[1]))[0, 1], np.corrcoef(np.hstack(shuffled_trials_block_1), np.hstack(power_ave_blocks[2]))[0, 1]]))

    p_value = (sum(mean_rho > actual_mean_rho) + 1) / (len(mean_rho) + 1)

    axs[0, 2].hist(mean_rho, 20,  normed=True)
    axs[0, 2].set_xlabel('Inter-block correlation', fontsize=24)
    axs[0, 2].set_ylabel('Normalized counts of permutated trials', fontsize=24)
    axs[0, 2].set_ylim([0, 40])
    # axs[0, 2].set_xlim([-0.5, 0.5])
    axs[0, 2].text(axs[0, 2].get_xlim()[0] + 0.1*(axs[0, 2].get_xlim()[1]- axs[0, 2].get_xlim()[0]), 38, 'rho (experiment)=' + "%.4f" % actual_mean_rho, color='k', fontsize=24)
    axs[0, 2].text(axs[0, 2].get_xlim()[0] + 0.1*(axs[0, 2].get_xlim()[1]- axs[0, 2].get_xlim()[0]), 33, 'p-value=' + "%.4f" % p_value, color='k', fontsize=24)

    axs[0, 2].legend(loc=1, fontsize=24)
    axs[0, 2].grid(True)
    print(tvalue, pvalue)

    # Plot blocks
    for block in range(3):
        if block == 0:
            vmax1 = np.nanpercentile(np.vstack(power_ave_blocks[block]), 95)
            vmin1 = np.nanpercentile(np.vstack(power_ave_blocks[block]), 5)

        map = axs[1, block].imshow(np.vstack(power_ave_blocks[block]), vmin=vmin1, vmax=vmax1, cmap='jet', aspect='auto')
        axs[1, block].set_title('Block ' + str(settings.blocks[block]))
        step = 100
        plt.setp(axs[1, block], xticks = range(0, power_ave_blocks[block][0].shape[0], step), xticklabels=[str(np.around(n,1)) for n in power.times[IX_timewindow][0::step]])
        axs[1, block].set_xlabel('Time [sec]', fontsize=16)
        axs[1, block].set_ylabel('Trial', fontsize=16)
        # if block == 2:
            # cbar = plt.colorbar(map, cax=axs[1, 2])
            # cbar.set_label(label='Power (dB)', size=16)

    plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Reproducability', file_name + '.png'))
