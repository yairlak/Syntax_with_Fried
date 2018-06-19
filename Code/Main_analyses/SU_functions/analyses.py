from __future__ import division
import numpy as np
import os
import mne
import matplotlib.pyplot as plt
import pickle
import matplotlib.image as mpimg
from operator import itemgetter

def generate_rasters(epochs_spikes, query, electrode_names_from_raw_files, from_channels, settings, params, preferences):
    for cluster in np.arange(epochs_spikes.info['nchan']):

        # Sort if needed
        if preferences.sort_according_to_key:
            fields_for_sorting = []
            for field in preferences.sort_according_to_key:
                fields_for_sorting.append(epochs_spikes.metadata[field])
            if len(fields_for_sorting) == 1:
                mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0])]
                IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
            elif len(fields_for_sorting) == 2:
                mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                                         fields_for_sorting[1])]
                IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
        else:
            IX = None

        fig = epochs_spikes.plot_image(cluster, order=IX , vmin=0, vmax=1, colorbar=False, show=False)

        if preferences.sort_according_to_key:
            fig[0].axes[0].set_yticks(range(0, len(fields_for_sorting[0]), preferences.step))
            yticklabels = np.sort(fields_for_sorting[0])[::preferences.step]
            yticklabels = yticklabels[::-1]
            fig[0].axes[0].set_yticklabels(yticklabels)
            plt.setp(fig[0].axes[0], ylabel=preferences.sort_according_to_key[0])

        sfreq = epochs_spikes.info['sfreq']
        gaussian_width = 20 * 1e-3
        mean_spike_count = np.mean(epochs_spikes._data[:,cluster,:], axis=0)
        new_y_smoothed = smooth_with_gaussian(mean_spike_count, sfreq, gaussian_width = gaussian_width * sfreq)  # smooth with 20ms gaussian

        x = fig[0].axes[1].lines[0]._x

        fig[0].axes[1].clear()

        fig[0].axes[1].plot(x, new_y_smoothed, 'k-')
        fig[0].axes[1].set_xlim([fig[0].axes[0].get_xlim()[0]/1000, fig[0].axes[0].get_xlim()[1]/1000])
        fig[0].axes[1].axvline(x=0, linestyle='--')

        plt.setp(fig[0].axes[1], ylim=[0, params.ylim_PSTH], xlabel = 'Time [sec]', ylabel='spikes / s')
        # IX = settings.events_to_plot[0].find('block')
        # fname = 'raster_' + settings.hospital + '_' + settings.patient + '_channel_' + str(from_channels[cluster]) \
        #         + '_cluster_' + str(cluster) + '_blocks_' + str(settings.blocks) + '_' + settings.events_to_plot[0][0:IX-1] + '_lengthSorted_' + \
        #         str(preferences.sort_according_to_sentence_length) + '_' + electrode_names_from_raw_files[cluster] + '.png'
        #         # )
        fname = 'raster_' + settings.hospital + '_' + settings.patient +  '_' + electrode_names_from_raw_files[cluster] + '_cluster_' + str(cluster) + '_' + query
        # )
        for key_sort in preferences.sort_according_to_key:
            fname += '_' + key_sort + 'Sorted'

        if not os.path.exists(os.path.join(settings.path2figures, settings.patient, 'Rasters')):
            os.makedirs(os.path.join(settings.path2figures, settings.patient, 'Rasters'))
        plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Rasters', fname + '.png'))


def average_high_gamma(epochs, band, fmin, fmax, fstep, baseline, baseline_type, params):
    freqs = np.arange(fmin, fmax, fstep)
    # -------------------------------
    # - delta_F =  2 * F / n_cycles -
    # - delta_T = n_cycles / F / pi -
    # - delta_T * delta_F = 2 / pi  -
    # -------------------------------
    # n_cycles = freq[0] / freqs * 3.14
    # n_cycles = freqs / 2.
    n_cycles = 7 # Fieldtrip's default
    if band == 'High-Gamma': n_cycles = 20

    power = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, n_jobs=4, average=False, n_cycles=n_cycles,
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
        # if all("KEY" in s for s in event_id_or_query):
        #     power_ave_baselined = power_ave
    else:
        if baseline_type == 'subtract_average':
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
            print("Baseline: subtract average")
        elif baseline_type == 'trial_wise':
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])
            print("Baseline: trial-wise")
        elif baseline_type == 'no_baseline':
            power_ave_baselined = power_ave  # don't apply any baseline

    # Gaussian smooth of time-freq results if chosen:
    if params.smooth_time_freq > 0:
        power_ave_baselined_smoothed = np.empty(power_ave_baselined.shape)
        for i in range(power_ave_baselined.shape[0]):
            power_ave_baselined_smoothed[i, :] = smooth_with_gaussian(power_ave_baselined[i, :], params.smooth_time_freq)
    else:
        power_ave_baselined_smoothed = power_ave_baselined

    return power, power_ave_baselined_smoothed, baseline


def plot_and_save_high_gamma(power, power_ave, align_to, blocks, probe_name, file_name, settings, params, preferences):
    from scipy import stats

    # Remove 0.2 sec from each side due to boundary effects
    IX_smaller_time_window = (power.times > power.tmin + 0.2) & (power.times < power.tmax - 0.2)  # relevant times
    power_ave = power_ave[:, IX_smaller_time_window]
    power_ave_zscore = stats.zscore(power_ave)
    power_ave[(power_ave_zscore > 3) | (power_ave_zscore < -3)] = np.NaN

    # Sort if needed
    if preferences.sort_according_to_key:
        fields_for_sorting = []
        for field in preferences.sort_according_to_key:
            fields_for_sorting.append(power.metadata[field])
        if len(fields_for_sorting) == 1:
            mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])),fields_for_sorting[0])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
        elif len(fields_for_sorting) == 2:
            mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                               fields_for_sorting[1])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
        power_ave = power_ave[IX, :]

    # Plot
    fig = plt.figure(figsize=(20, 12))
    ax0 = plt.subplot2grid((12, 13), (0, 0), rowspan=10, colspan=10)
    ax1 = plt.subplot2grid((12, 13), (0, 10), rowspan=10, colspan=2)
    ax2 = plt.subplot2grid((12, 13), (10, 0), rowspan=2, colspan=10)
    cbaxes = plt.subplot2grid((12, 13), (0, 12), rowspan=10)

    vmax1 = np.nanpercentile(power_ave, 95)
    vmin1 = np.nanpercentile(power_ave, 5)
    map = ax0.imshow(power_ave,
                     extent=[np.min(power.times)+0.2, np.max(power.times)-0.2, 1, power.data.shape[0] + 1],
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


    IX = (power.times > params.window_st / 1e3) & (power.times < params.window_ed / 1e3)
    ax1.plot(np.nanmean(power_ave[:, IX], axis=1), np.arange(1, 1 + power_ave.shape[0]))
    ax1.set_xlabel('Mean activity')
    ax1.set_ylim([1, 1 + power_ave.shape[0]])
    ax1.set_xlim([0, np.nanmean(power_ave) + 3*np.nanstd(power_ave)])
    ax1.tick_params(axis='y', which='both', left='off', labelleft='off', direction='in')

    IX_smaller_time_window = (power.times > min(power.times) + 0.2) & (power.times < max(power.times) - 0.2)  # indices to relevant times
    ax2.plot(power.times[IX_smaller_time_window], stats.zscore(np.nanmean(power_ave, axis=0)))
    ax2.set_xlabel('Time [sec]', fontsize=24)
    ax2.set_ylabel('Mean activity (zscore)', fontsize=18)
    ax2.set_xlim([np.min(power.times)+0.2, np.max(power.times)-0.2])
    ax2.axhline(y=3, linestyle='--', linewidth=3, color='g')
    ax2.axhline(y=-3, linestyle='--', linewidth=3, color='g')
    ax2.set_ylim([-6, 6])

    # ax2_2 = ax2.twinx()
    # ax2_2.plot(power.times[IX_smaller_time_window], stats.zscore(np.nanmean(power_ave, axis=0)))
    # ax2_2.set_ylabel('zscore', color='b')
    # ax2_2.tick_params('y', colors='b')
    # ax2_2.axhline(y=3, linestyle='--', linewidth=3, color='b')
    # ax2_2.axhline(y=-3, linestyle='--', linewidth=3, color='b')

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

    # import pickle
    # with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name + '.pkl'), 'w') as f:
    #     pickle.dump([power, settings, params, preferences], f)


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


def smooth_with_gaussian(time_series, sfreq, gaussian_width = 50, N=1000):
    # gaussian_width in samples
    # ---------------------
    import math
    from scipy import signal
    norm_factor = np.sqrt(2 * math.pi * gaussian_width ** 2)/sfreq # sanity check: norm_factor = gaussian_window.sum()
    gaussian_window = signal.general_gaussian(M=N, p=1, sig=gaussian_width) # generate gaussian filter
    norm_factor = (gaussian_window/sfreq).sum()
    smoothed_time_series = np.convolve(time_series, gaussian_window/norm_factor, mode="full") # smooth
    smoothed_time_series = smoothed_time_series[int(round(N/2)):-(int(round(N/2))-1)] # trim ends
    return smoothed_time_series
