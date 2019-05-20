from __future__ import division
import numpy as np
import os
import mne
import matplotlib.pyplot as plt
import pickle
from operator import itemgetter
from functions import load_data, convert_to_mne
from functions.auxilary_functions import  smooth_with_gaussian
from functions.auxilary_functions import  get_queries


def generate_raster_plots(events_spikes, event_id, metadata, comparisons, settings, params, preferences):
    print('Loading spike sorted data (spike clusters)...')
    spikes, settings, electrode_names_from_raw_files, from_channels = load_data.spike_clusters(settings)

    print('Generating MNE raw object for spikes...')
    raw_spikes = convert_to_mne.generate_mne_raw_object_for_spikes(spikes, electrode_names_from_raw_files, settings,
                                                                   params)

    print('Epoching spiking data...')
    epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, metadata=metadata,
                               baseline=None, preload=True)
    print(epochs_spikes)

    print('Generate rasters and PSTHs...')

    if preferences.use_metadata_only:
        for i, comparison in enumerate(comparisons):
            print('Contrast: ' + comparison['contrast_name'])
            queries = get_queries(comparison)
            preferences.sort_according_to_key = [s.strip().encode('ascii') for s in comparison['sorting']]
            for query in queries:
                print('Query: ' + query)
                generate_rasters(epochs_spikes[query], query, electrode_names_from_raw_files, from_channels,
                                          settings, params, preferences)

                if preferences.save_features_for_classification:
                    # Save rasters as features for classifcation
                    file_name = 'Feature_matrix_rasters_' + settings.patient + '_' + query
                    if not os.path.exists(
                        os.path.join(settings.path2output, settings.patient, 'feature_matrix_for_classification')): os.makedirs(
                        os.path.join(settings.path2output, settings.patient, 'feature_matrix_for_classification'))
                    with open(os.path.join(settings.path2output, settings.patient, 'feature_matrix_for_classification',
                                           file_name + '.pkl'), 'wb') as f:
                        pickle.dump([epochs_spikes[query], electrode_names_from_raw_files, query, settings, params, preferences], f)

                    print('Data saved to: ' + os.path.join(settings.path2output, settings.patient,
                                                           'feature_matrix_for_classification',
                                                           file_name + '.pkl'))


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
        fname = 'raster_' + settings.hospital + '_' + settings.patient +  '_' + electrode_names_from_raw_files[cluster] + '_cluster_' + str(cluster) + '_' + query

        for key_sort in preferences.sort_according_to_key:
            fname += '_' + key_sort + 'Sorted'

        if not os.path.exists(os.path.join(settings.path2figures, settings.patient, 'Rasters')):
            os.makedirs(os.path.join(settings.path2figures, settings.patient, 'Rasters'))
        plt.savefig(os.path.join(settings.path2figures, settings.patient, 'Rasters', fname + '.png'))
        plt.close()



