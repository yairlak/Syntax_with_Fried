from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, analyses
from scipy import io
import os
import numpy as np

# Following Ariel's setup, this function generates CSC_cluster?.mat files according to the output of Wave_Clus.
# It adds time0 and timeend vars, which are important for the synchronization between the paradigm log files and
# the recordings.


def generate_spike_csc_cluster_files(data_all_channels_spike_clusters, channel_numbers, electrode_names, settings):
    cnt = 1
    for i, ch in enumerate(settings.channels_with_spikes):
        if ch in channel_numbers:
            curr_channel_clusters = data_all_channels_spike_clusters[ch - 1]

            clusters = list(set(curr_channel_clusters[:, 0].astype('int')))
            for cluster in clusters:
                if cluster > 0: # TODO: check if cluster #0 in wave_clus output corresponds to the 'garabage' cluster
                    curr_cluster_spike_times = curr_channel_clusters[curr_channel_clusters[:, 0] == cluster, 1]
                    curr_cluster_spike_times_in_sec = curr_cluster_spike_times/1e3

                    temp_dict = {}
                    temp_dict['spike_times_sec'] = np.asarray(curr_cluster_spike_times_in_sec)
                    temp_dict['time0'] = settings.time0
                    temp_dict['timeend'] = settings.timeend
                    temp_dict['electrode_name'] = electrode_names[ch-1]
                    temp_dict['from_channel'] = ch

                    filename_curr_cluster = 'CSC' + str(cnt) + '_cluster.mat'
                    if not os.path.exists(settings.path2output_spike_clusters):
                        os.makedirs(settings.path2output_spike_clusters)
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
