import numpy as np
import os
import neo
#from neo.io import BlackrockIO
import mne
import matplotlib.pyplot as plt
import scipy
import glob
import sys
from scipy import io


def generate_rasters(epochs_spikes, settings):
    for cluster in np.arange(epochs_spikes.info['nchan']):
        fig = epochs_spikes[settings.events_to_plot].plot_image(cluster, vmin=0, vmax=1, colorbar=False, show=False)
        plt.setp(fig[0].axes[1], ylim=[0, None], ylabel='spikes / s')
        fname = 'raster_' + settings.hospital + '_' + settings.patient + '_' + str(cluster) + str(
            settings.blocks) + '.png'
        plt.savefig(os.path.join(settings.path2figures, 'Rasters', fname))


def average_high_gamma(epochs, event_id, band, fmin, fmax, fstep):
    print('Time-freq...')
    freqs = np.arange(fmin, fmax, fstep)
    n_cycles = freqs / 2
    power = mne.time_frequency.tfr_morlet(epochs[event_id], freqs=freqs, n_jobs=30, average=False, n_cycles=n_cycles,
                                          return_itc=False, picks=[0])
    power_ave = np.squeeze(np.average(power.data, axis=2))
    return power, power_ave


def plot_and_save_average_freq_band(power1, power2, power_ave1, power_ave2, event_id_1, event_id_2, file_name):

    fig, axs = plt.subplots(2, 1, figsize=(6, 6))
    cnt = 0
    for ax in axs.reshape(-1):
        if cnt == 0:
            vmax1 = np.mean(power_ave1) + 1 * np.std(power_ave1)
            map = ax.imshow(power_ave1,
                            extent=[np.min(power1.times), np.max(power1.times), 1, power1.data.shape[0] + 1],
                            interpolation='nearest',
                            aspect='auto', vmin=0, vmax=vmax1)
            plt.colorbar(map, ax=ax, label='Power')
            ax.set_title(event_id_temp[0][0])
            ax.set_ylabel('Trial')
        elif cnt == 1:
            vmax2 = np.mean(power_ave2) + 1 * np.std(power_ave2)
            map1 = ax.imshow(power_ave2,
                             extent=[np.min(power2.times), np.max(power2.times), 1, power2.data.shape[0] + 1],
                             interpolation='nearest',
                             aspect='auto', vmin=0, vmax=vmax2)
            ax.set_title(event_id_temp[1][0])
            plt.colorbar(map1, ax=ax, label='Power')
            ax.set_ylabel('Trial')
            ax.set_xlabel('Time [sec]')
        cnt += 1

    fig.savefig(os.path.join('..', 'Figures', 'HighGamma', file_name))
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
