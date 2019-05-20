import numpy as np
import mne


def generate_events_array(metadata, params):
    '''

    :param metadata: (pandas dataframe) num_words X num_features; all words across all stimuli
    :param params: (object) general parameters
    :return:
    '''

    # First column of events object
    curr_times = params.sfreq_raw * metadata['event_time'].values
    curr_times = np.expand_dims(curr_times, axis=1)

    # Second column
    second_column = np.zeros((len(curr_times), 1))

    # Third column
    event_numbers = 100 * metadata['block'].values  # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
    event_type_names = ['block_' + str(i) for i in metadata['block'].values]
    event_numbers = np.expand_dims(event_numbers, axis=1)

    # EVENT object: concatenate all three columns together (then change to int and sort)
    events = np.hstack((curr_times, second_column, event_numbers))
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    # EVENT_ID dictionary: mapping block names to event numbers
    event_id = dict([(event_type_name, event_number[0]) for event_type_name, event_number in zip(event_type_names, event_numbers)])

    # Generate another event object for single-unit data (which has a different sampling rate)
    events_spikes = np.copy(events)
    events_spikes[:, 0] = events_spikes[:, 0] * params.sfreq_spikes / params.sfreq_raw
    events_spikes = events_spikes.astype(np.int64)

    return events, events_spikes, event_id

def generate_mne_raw_object(data, settings, params):
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    info = mne.create_info(ch_names=[settings.channel_name], sfreq=params.sfreq_raw, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    return raw

def generate_mne_raw_object_for_spikes(spikes, electrode_names, settings, params):
    sfreq = params.sfreq_spikes
    num_channels = len(spikes)
    ch_types = ['seeg' for s in range(num_channels)]

    # montage = mne.channels.read_montage(kind='filename', ch_names=None, path='datapath', unit='m', transform=False)
    # print(montage)
    # raw.set_montage(montage, set_dig=True)
    # montage = mne.channels.read_montage('standard_1005')
    # montage.selection = montage.selection[0:len(electrode_names)]
    # montage.ch_names[0:len(electrode_names)] = electrode_names

    info = mne.create_info(ch_names=electrode_names, sfreq=sfreq, ch_types=ch_types)

    num_samples = 1+int(sfreq * (settings.timeend - settings.time0)/1e6) # Use same sampling rate as for macro, just for convenience.
    spikes_matrix_all_clusters = np.empty((0, num_samples))
    for cluster, curr_spike_times in enumerate(spikes):
        spikes_zero_one_vec = np.zeros(num_samples) # convert to samples from sec
        curr_spike_times = (curr_spike_times - settings.time0 / 1e6) * sfreq # convert to samples from sec
        curr_spike_times = curr_spike_times.astype(np.int64)
        spikes_zero_one_vec[curr_spike_times] = 1
        spikes_matrix_all_clusters = np.vstack((spikes_matrix_all_clusters, spikes_zero_one_vec))
    raw = mne.io.RawArray(spikes_matrix_all_clusters, info)
    return raw