import numpy as np
import os
import mne
import matplotlib.pyplot as plt
import pickle
import matplotlib.image as mpimg


def generate_rasters(epochs_spikes, log_all_blocks, electrode_names_from_raw_files, from_channels, settings, params, preferences):
    for cluster in np.arange(epochs_spikes.info['nchan']):
        if preferences.sort_according_to_sentence_length:
            sentences_length = []
            for log in log_all_blocks:
                sentences_length = sentences_length + log.sentences_length.values()
            order = np.argsort(sentences_length)
        else:
            order = None

        fig = epochs_spikes[settings.events_to_plot].plot_image(cluster, order=order , vmin=0, vmax=1, colorbar=False, show=False)

        if preferences.sort_according_to_sentence_length:
            fig[0].axes[0].set_yticks(range(0,len(sentences_length), preferences.step))
            sent_len = np.sort(sentences_length)[::preferences.step]
            # sent_len = sent_len[::-1]
            fig[0].axes[0].set_yticklabels(sent_len)
            plt.setp(fig[0].axes[0], ylabel = 'Sentence length')

        new_y = fig[0].axes[1].lines[0]._y/epochs_spikes[settings.events_to_plot].events.shape[0]
        new_y_smoothed = smooth_with_gaussian(new_y, gaussian_width=20*1e-3*params.sfreq_spikes) # smooth with 20ms gaussian
        x = fig[0].axes[1].lines[0]._x

        fig[0].axes[1].clear()

        fig[0].axes[1].plot(x, new_y_smoothed, 'k-')
        fig[0].axes[1].set_xlim([fig[0].axes[0].get_xlim()[0]/1000, fig[0].axes[0].get_xlim()[1]/1000])
        fig[0].axes[1].axvline(x=0, linestyle='--')

        plt.setp(fig[0].axes[1], ylim=[0, params.ylim_PSTH], xlabel = 'Time [sec]', ylabel='spikes / s')
        IX = settings.events_to_plot[0].find('block')
        fname = 'raster_' + settings.hospital + '_' + settings.patient + '_channel_' + str(from_channels[cluster]) \
                + '_cluster_' + str(cluster) + '_blocks_' + str(settings.blocks) + '_' + settings.events_to_plot[0][0:IX-1] + '_lengthSorted_' + \
                str(preferences.sort_according_to_sentence_length) + '_' + electrode_names_from_raw_files[cluster] + '.png'
                # )
        plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Rasters', fname))


def average_high_gamma(epochs, event_id, band, fmin, fmax, fstep, baseline, baseline_type, params):
    print('Time-freq...')
    freqs = np.arange(fmin, fmax, fstep)
    temporal_resolution = 0.05 # in [sec]
    n_cycles = freqs * 3.14 * temporal_resolution
    power = mne.time_frequency.tfr_morlet(epochs[event_id], freqs=freqs, n_jobs=30, average=False, n_cycles=n_cycles,
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
        if all("KEY" in s for s in event_id):
            power_ave_baselined = power_ave
    else:
        if baseline_type == 'subtract_average':
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
	    print("Baseline: subtract average")
        elif baseline_type == 'trial_wise':
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])
	    print("Baseline: trial-wise")
        elif baseline_type == 'no_baseline':
            power_ave_baselined = power_ave  # don't apply any baseline

    # Remove 0.2 sec from each side due to boundary effects
    IX_smaller_time_window = (epochs.times > epochs.tmin + 0.2) & (epochs.times < epochs.tmax - 0.2)  # indices to relevant times
    power_ave_baselined = power_ave_baselined[:, IX_smaller_time_window]

    return power, power_ave_baselined, baseline


def plot_and_save_high_gamma(power, power_ave, event_str, log_all_blocks, word2pos, file_name, settings, params, preferences):
    from scipy import stats
    power_ave_zscore = stats.zscore(power_ave)
    power_ave[(power_ave_zscore > 3) | (power_ave_zscore < -3)] = np.NaN

    if "KEY" not in event_str:
        if preferences.sort_according_to_sentence_length:
            sentences_length = []
            for log in log_all_blocks:
                sentences_length = sentences_length + log.sentences_length.values()
            order = np.argsort(sentences_length)
            power_ave = power_ave[order, :]
        elif preferences.sort_according_to_num_letters:
                num_letters = []
                for log in log_all_blocks:
                    num_letters = num_letters + log.num_letters
                order = np.argsort(num_letters)
                power_ave = power_ave[order, :]
        elif preferences.sort_according_to_pos:
            all_words_pos = []
            for log in log_all_blocks:
                attribute_word_string = [s for s in dir(log) if "_STRING" in s][0]
                curr_pos = [word2pos[w[0:-1].lower()] if w[-1] == '?' or w[-1] == '.' else word2pos[w.lower()] for w in
                            getattr(log, attribute_word_string)]
                all_words_pos = all_words_pos + curr_pos
            order = np.argsort(all_words_pos)
            power_ave = power_ave[order, :]
        else:
            order = None

    # IX = settings.events_to_plot[0].find('block')
    # title = settings.events_to_plot[0][0:IX-1]
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
    # cbar = plt.colorbar(map, ax=ax0)
    cbar.set_label(label='Power (dB)', size=22)
    # cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8])

    ax0.set_title('Aligned to ' + event_str, fontsize=24)
    ax0.set_ylabel('Trial', fontsize=24)
    ax0.tick_params(axis='x', which='both', bottom='off', labelbottom='off')

    if preferences.sort_according_to_sentence_length:
        ax0.set_yticks(range(0, len(sentences_length), preferences.step))
        sent_len = np.sort(sentences_length)[::preferences.step]
        sent_len = sent_len[::-1]
        ax0.set_yticklabels(sent_len)
        plt.setp(ax0, ylabel='Sentence length')
    elif preferences.sort_according_to_num_letters:
        ax0.set_yticks(range(0, len(num_letters), preferences.step))
        num_letters_str = np.sort(num_letters)[::preferences.step]
        num_letters_str = num_letters_str[::-1]
        ax0.set_yticklabels(num_letters_str)
        plt.setp(ax0, ylabel='Number of letters')
    elif preferences.sort_according_to_pos:
        ax0.set_yticks(range(0, len(all_words_pos), preferences.step))
        word_pos_sorted = np.asarray(all_words_pos)[order]
	word_pos_sorted = word_pos_sorted[::preferences.step]
	word_pos_sorted = word_pos_sorted[::-1]
        ax0.set_yticklabels(word_pos_sorted)
        plt.setp(ax0, ylabel='Part of Speech')

    IX = (power.times > params.window_st / 1e3) & (power.times < params.window_ed / 1e3)
    ax1.plot(np.nanmean(power_ave[:, IX], axis=1), np.arange(1, 1 + power_ave.shape[0]))
    ax1.set_xlabel('Mean activity')
    ax1.set_ylim([1, 1 + power_ave.shape[0]])
    ax1.set_xlim([0, np.nanmean(power_ave) + 3*np.nanstd(power_ave)])
    ax1.tick_params(axis='y', which='both', left='off', labelleft='off', direction='in')

    IX_smaller_time_window = (power.times > min(power.times) + 0.2) & (power.times < max(power.times) - 0.2)  # indices to relevant times
    ax2.plot(power.times[IX_smaller_time_window], np.nanmean(power_ave, axis=0))
    ax2.set_xlabel('Time [sec]', fontsize=24)
    ax2.set_ylabel('Mean activity', fontsize=18)
    ax2.set_xlim([np.min(power.times)+0.2, np.max(power.times)-0.2])

    # Add vertical lines
    ax0.axvline(x=0, linestyle='--', linewidth=3, color='k')
    ax2.axvline(x=0, linestyle='--', linewidth=3, color='k')
    if event_str == "FIRST_WORD" and (set(settings.blocks) & set([1,3,5])):
        ax0.axvline(x=params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
    elif event_str == "LAST_WORD" and (set(settings.blocks) & set([1,3,5])):
        ax0.axvline(x=-params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=-2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax0.axvline(x=-3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-2 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        ax2.axvline(x=-3 * params.SOA * 1e-3, linestyle='--', linewidth=1, color='b')

    print('Saving as - ' + os.path.join(settings.path2figures, settings.patient, 'HighGamma', file_name + '.png'))
    fig.savefig(os.path.join(settings.path2figures, settings.patient, 'HighGamma', file_name + '.png'))
    plt.close(fig)

    # import pickle
    # with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name + '.pkl'), 'w') as f:
    #     pickle.dump([power, settings, params, preferences], f)


def plot_and_save_average_freq_band(power1, power2, power3, power_ave1, power_ave2, power_ave3, event_id_1, event_id_2, event_id_3, file_name, fig_paradigm, settings, log_all_blocks, preferences):
    if preferences.sort_according_to_sentence_length:
        sentences_length = []
        for log in log_all_blocks:
            sentences_length = sentences_length + log.sentences_length.values()
        order = np.argsort(sentences_length)
        power_ave1 = power_ave1[order, :]
        power_ave3 = power_ave3[order, :]
    else:
        order = None

    IX = settings.events_to_plot[0].find('block')
    title = settings.events_to_plot[0][0:IX-1]
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))
    cnt = 0
    for ax in axs.reshape(-1):
        if cnt == 0:
            vmax1 = np.percentile(power_ave1, 95)
            vmin1 = np.percentile(power_ave1, 5)
            map = ax.imshow(power_ave1,
                            extent=[np.min(power1.times), np.max(power1.times), 1, power1.data.shape[0] + 1],
                            interpolation='nearest',
                            aspect='auto', vmin=vmin1, vmax=vmax1)
            plt.colorbar(map, ax=ax, label='Power (dB)')
            # ax.set_title('Locked to first word')
            ax.set_ylabel('Trial')
            ax.axvline(x=0, linestyle='--', linewidth=3, color='k')
            ax.axvline(x=settings.SOA*1e-3, linestyle='--', linewidth=1, color='k')
            ax.axvline(x=2*settings.SOA*1e-3, linestyle='--', linewidth=1, color='b')
            ax.axvline(x=3 * settings.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            if preferences.sort_according_to_sentence_length:
                ax.set_yticks(range(0, len(sentences_length), preferences.step))
                sent_len = np.sort(sentences_length)[::preferences.step]
                sent_len = sent_len[::-1]
                ax.set_yticklabels(sent_len)
                plt.setp(ax, ylabel='Sentence length')

        elif cnt == 1:
            vmax2 = np.percentile(power_ave2, 95)
            vmin2 = np.percentile(power_ave2, 5)
            map2 = ax.imshow(power_ave2,
                             extent=[np.min(power2.times), np.max(power2.times), 1, power2.data.shape[0] + 1],
                             interpolation='nearest',
                             aspect='auto', vmin=vmin2, vmax=vmax2)
            ax.set_title('Key press (food related)')
            plt.colorbar(map2, ax=ax, label='Power (dB)')
            ax.set_ylabel('Trial')
            ax.set_xlabel('Time [sec]')
            ax.axvline(x=0, linestyle='--', linewidth=3, color='k')
            ax.axvline(x=settings.SOA * 1e-3, linestyle='--', linewidth=1, color='k')
            ax.axvline(x=2 * settings.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax.axvline(x=3 * settings.SOA * 1e-3, linestyle='--', linewidth=1, color='b')

        elif cnt == 2:
            vmax3 = np.percentile(power_ave3, 95)
            vmin3 = np.percentile(power_ave3, 5)
            map3 = ax.imshow(power_ave3,
                             extent=[np.min(power3.times), np.max(power3.times), 1, power3.data.shape[0] + 1],
                             interpolation='nearest',
                             aspect='auto', vmin=vmin3, vmax=vmax3)
            ax.set_title('Locked to last word')
            # ax.set_title('Locked to end of wav file')
            plt.colorbar(map3, ax=ax, label='Power (dB)')
            ax.set_ylabel('Trial')
            ax.set_xlabel('Time [sec]')
            ax.axvline(x=0, linestyle='--', linewidth=3, color='k')
            ax.axvline(x=-settings.SOA * 1e-3, linestyle='--', linewidth=1, color='k')
            ax.axvline(x=-2 * settings.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax.axvline(x=-3 * settings.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            if preferences.sort_according_to_sentence_length:
                ax.set_yticks(range(0, len(sentences_length), preferences.step))
                sent_len = np.sort(sentences_length)[::preferences.step]
                sent_len = sent_len[::-1]
                ax.set_yticklabels(sent_len)
                plt.setp(ax, ylabel='Sentence length')
        elif cnt == 3:
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '_' + str(settings.blocks) + '.png'
            img = mpimg.imread(os.path.join(settings.path2figures, settings.patient, 'misc', fname))
            plt.imshow(img)

        cnt += 1

    fig.savefig(os.path.join(settings.path2figures, settings.patient, 'HighGamma', file_name))
    plt.close(fig)




    # event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
    # power1 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_1], freqs=freqs, n_jobs=30, average=False, n_cycles=n_cycles,
    #                                       return_itc=False, picks=[0])
    #
    # event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
    # power2 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_2], freqs=freqs, n_jobs=30, average=False,
    #                                        n_cycles=n_cycles,
    #                                        return_itc=False, picks=[0])
    #
    # power_ave1 = np.squeeze(np.average(power1.data, axis=2))
    # power_ave2 = np.squeeze(np.average(power2.data, axis=2))
    #
    # file_name = band + '_Patient_' + settings.file_stem + '_Channel_' + str(channel + 1) + '_Event_id' + str(
    #     epochs_resampled.event_id.values()) + settings.channel_name + '.png'
    # fig, axs = plt.subplots(2, 1, figsize=(6, 6))
    # cnt = 0
    # for ax in axs.reshape(-1):
    #     if cnt == 0:
    #         vmax1 = np.mean(power_ave1) + 1 * np.std(power_ave1)
    #         map = ax.imshow(power_ave1, extent=[np.min(power1.times), np.max(power1.times), 1, power1.data.shape[0] + 1],
    #                     interpolation='nearest',
    #                     aspect='auto', vmin=0, vmax=vmax1)
    #         plt.colorbar(map, ax=ax, label='Power')
    #         ax.set_title(event_id_temp[0][0])
    #         ax.set_ylabel('Trial')
    #     elif cnt ==1:
    #         vmax2 = np.mean(power_ave2) + 1 * np.std(power_ave2)
    #         map1 = ax.imshow(power_ave2,
    #                         extent=[np.min(power2.times), np.max(power2.times), 1, power2.data.shape[0] + 1],
    #                         interpolation='nearest',
    #                         aspect='auto', vmin=0, vmax=vmax2)
    #         ax.set_title(event_id_temp[1][0])
    #         plt.colorbar(map1, ax=ax, label='Power')
    #         ax.set_ylabel('Trial')
    #         ax.set_xlabel('Time [sec]')
    #     cnt += 1
    #
    # fig.savefig(os.path.join('..', '..', 'Figures', 'HighGamma', file_name))
    # plt.close(fig)


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    y = y[(window_len / 2):-(window_len / 2)]
    return y


def smooth_with_gaussian(time_series, gaussian_width = 50, N=1000):
    # gaussian_width in ms
    # ---------------------
    import math
    from scipy import signal
    norm_factor = np.sqrt(2 * math.pi * gaussian_width ** 2) # sanity check: norm_factor = gaussian_window.sum()
    gaussian_window = signal.general_gaussian(M=N, p=1, sig=gaussian_width) # generate gaussian filter
    smoothed_time_series = np.convolve(time_series, gaussian_window/norm_factor, mode="full") # smooth
    smoothed_time_series = smoothed_time_series[int(round(N/2)):-(int(round(N/2))-1)] # trim ends
    return smoothed_time_series
