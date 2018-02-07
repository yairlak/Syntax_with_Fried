from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, analyses
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np

# Following Ariel's setup, this function generates CSC_cluster?.mat files according to the output of Wave_Clus.
# It adds time0 and timeend vars, which are important for the synchronization between the paradigm log files and
# the recordings.


def generate_spike_csc_cluster_files(data_all_channels_spike_clusters, channel_numbers, electrode_names, settings):
    cnt = 1
    for i, ch in enumerate(settings.channels_with_spikes):
        if ch in channel_numbers:
            curr_channel_clusters = data_all_channels_spike_clusters[ch - 1]

            num_of_spike_clusters = int(np.max(curr_channel_clusters[:, 0]))
            for cluster in range(num_of_spike_clusters):
                spike_times_sec = []
                for spike in range(curr_channel_clusters.shape[0]):
                    curr_cluster_number = int(curr_channel_clusters[spike][0] - 1)  # Change the ZERO-based indexing
                    curr_cluster_time = curr_channel_clusters[spike][1]
                    curr_cluster_time = curr_cluster_time / 1e3  # change to sec as in Ariel's files
                    if curr_cluster_number == cluster:
                        spike_times_sec.append(curr_cluster_time)

                temp_dict = {}
                temp_dict['spike_times_sec'] = np.asarray(spike_times_sec)
                temp_dict['time0'] = settings.time0
                temp_dict['timeend'] = settings.timeend
                temp_dict['electrode_name'] = electrode_names[ch-1]

                filename_curr_cluster = 'CSC' + str(cnt) + '_cluster.mat'
                io.savemat(os.path.join(settings.path2output_spike_clusters, filename_curr_cluster), temp_dict)
                print('Saved:' + filename_curr_cluster)
                cnt += 1  # To next cluster number in filename_curr_cluster
        else:
            print(
            'Error: settings.channels_with_spikes contains channels without a corresponding times file from Wave_clus')

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print('Loading settings...')
settings = load_settings_params.Settings()

print('Loading data...')
data_all_channels_spike_clusters, channel_numbers, settings = load_data.wave_clus_output_files(settings)

print('Loading electrode names...')
electrode_names = load_data.electrodes_names(settings)

print('Generating CSC_cluster files based on Wave_clus output (times_*.mat files)...')
generate_spike_csc_cluster_files(data_all_channels_spike_clusters, channel_numbers, electrode_names, settings)
