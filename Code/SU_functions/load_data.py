import os, glob
from scipy import io
import mne
import numpy as np


# Raw data
def raw_in_matlab_format(settings):
    CSC_file = glob.glob(os.path.join(settings.path2rawdata_mat, 'CSC' + str(settings.channel) + '.mat'))
    data_all = io.loadmat(CSC_file[0])['data']
    settings.channel_name = io.loadmat(CSC_file[0])['file_name'][0]
    return data_all, settings


def generate_mne_raw_object(data, settings, params):
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    #ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=[settings.channel_name], sfreq=params.sfreq_raw, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    return raw


# Spike-sorted data
def spike_clusters(settings):
    CSC_cluster_files = glob.glob(os.path.join(settings.path2spike_clusters, 'CSC*_cluster.mat'))
    data_all = []
    electrode_names_from_raw_files = []
    for cluster in CSC_cluster_files:
        data_all.append(io.loadmat(cluster)['spike_times_sec'])
        settings.time0 = io.loadmat(cluster)['time0'][0,0]
        settings.timeend = io.loadmat(cluster)['timeend'][0,0]
        electrode_names_from_raw_files.append(io.loadmat(cluster)['electrode_name'][0])

    electrode_names = cluster_to_electrode_name(settings)

    return data_all, settings, electrode_names, electrode_names_from_raw_files


def generate_mne_raw_object_for_spikes(spikes, electrode_names, settings, params):
    sfreq = params.sfreq_spikes
    num_channels = len(spikes)
    ch_types = ['seeg' for s in range(num_channels)]
    #ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=electrode_names, sfreq=sfreq, ch_types=ch_types)

    num_samples = 1+int(sfreq * (settings.timeend - settings.time0)/1e6) # Use same sampling rate as for macro, just for convenience.
    spikes_matrix_all_clusters = np.empty((0, num_samples))
    for cluster, curr_spike_times in enumerate(spikes):
        spikes_zero_one_vec = np.zeros(num_samples) # convert to samples from sec
        curr_spike_times = (curr_spike_times - settings.time0 / 1e6) * sfreq # same
        curr_spike_times = curr_spike_times.astype(np.int64)
        spikes_zero_one_vec[curr_spike_times] = 1
        spikes_matrix_all_clusters = np.vstack((spikes_matrix_all_clusters, spikes_zero_one_vec))
    raw = mne.io.RawArray(spikes_matrix_all_clusters, info)
    return raw

def wave_clus_output_files(settings):
    # Find all times_*.mat files in the output folder from Wave_clus
    times_files = glob.glob(os.path.join(settings.path2rawdata_mat, 'times_CSC*.mat'))

    # Extract the numbers of the channels found
    channel_numbers = []
    data_all_channels_spike_clusters = [None] * 1000 # Assuming never more than 1000 channels
    for channel_filename in times_files:
        curr_channel_number = int(''.join([s for s in os.path.basename(channel_filename) if s.isdigit()]))
        channel_numbers.append(curr_channel_number)
        # ZERO-based indexing
        data_all_channels_spike_clusters[curr_channel_number-1] = io.loadmat(channel_filename)['cluster_class']
        try:
            settings.time0 = io.loadmat(channel_filename)['time0'][0,0]
            settings.timeend = io.loadmat(channel_filename)['timeend'][0,0]
        except:
            print(channel_filename)

    return data_all_channels_spike_clusters, channel_numbers, settings

# Auxilary functions
def cluster_to_electrode_name(settings):
    with open(os.path.join(settings.path2log, 'clusters_electrode_montage.m')) as f:
        electrode_names = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        electrode_names = [x.strip().split("\t") for x in electrode_names if "\t" in x]
    for ele in range(len(electrode_names)):
        electrode_names[ele][0] = electrode_names[ele][0][:-1]
        electrode_names[ele][1] = ''.join([x for x in electrode_names[ele][1] if (x != "'" and x != ",")])
    electrode_names_list = [None] * 1000
    for ele in range(len(electrode_names)):
        for IX in electrode_names[ele][0].split(":"):
            electrode_names_list[int(IX)-1] = electrode_names[ele][1]

    return electrode_names_list


def electrodes_names(settings):
    electrode_names = io.loadmat(os.path.join(settings.path2patient_folder, 'electrodes_info_names.mat'))['electrodes_info'][0]
    np.ndarray.tolist(electrode_names)
    electrode_names = [s[0] for s in electrode_names]
    return electrode_names
