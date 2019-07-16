import os, glob
import numpy as np
import mne
from scipy import io

def get_channel_nums(path2rawdata):
    CSC_files = glob.glob(os.path.join(path2rawdata, 'micro', 'ChannelsCSC', 'CSC?.mat')) + \
                glob.glob(os.path.join(path2rawdata, 'micro', 'ChannelsCSC', 'CSC??.mat')) + \
                glob.glob(os.path.join(path2rawdata, 'micro', 'ChannelsCSC', 'CSC???.mat'))
    return [int(os.path.basename(s)[3:-4]) for s in CSC_files]


def load_channelsCSC_data(path2rawdata, channel):
    CSC_file = glob.glob(os.path.join(path2rawdata, 'micro', 'ChannelsCSC', 'CSC' + str(channel) + '.mat'))
    print(CSC_file)
    channel_data = io.loadmat(CSC_file[0])['data']
    print('channel-data loaded')
    if 'file_name' in io.loadmat(CSC_file[0]).keys():
        channel_name = io.loadmat(CSC_file[0])['file_name'][0]
    else:
        channel_name = 'Channel_'+str(channel)
    return channel_data, channel_name


def load_macro_data(path2rawdata, probe_name):
    macro1_data = []; macro2_data = []; macro3_data = []; macro4_data = []
    CSC_files = glob.glob(os.path.join(path2rawdata, 'macro', 'ChannelsCSC', 'CSC*.mat'))
    for CSC_file in sorted(CSC_files):
        channel_name = io.loadmat(CSC_file)['file_name'][0]
        if str(channel_name) == probe_name + '1.ncs':
            print(CSC_file)
            macro1_data = io.loadmat(CSC_file)['data']
            print('channel-data loaded')
        if str(channel_name) == probe_name + '2.ncs':
            print(CSC_file)
            macro2_data = io.loadmat(CSC_file)['data']
            print('channel-data loaded')
        if str(channel_name) == probe_name + '3.ncs':
            print(CSC_file)
            macro3_data = io.loadmat(CSC_file)['data']
            print('channel-data loaded')
        if str(channel_name) == probe_name + '4.ncs':
            print(CSC_file)
            macro4_data = io.loadmat(CSC_file)['data']
            print('channel-data loaded')

    return [macro1_data, macro2_data, macro3_data, macro4_data]

def add_event_to_metadata(metadata, event_time, sentence_number, sentence_string, word_position, word_string, pos, num_words, last_word):
    metadata['event_time'].append(event_time)
    metadata['sentence_number'].append(sentence_number)
    metadata['sentence_string'].append(sentence_string)
    metadata['word_position'].append(word_position)
    metadata['word_string'].append(word_string)
    metadata['pos'].append(pos)
    metadata['num_words'].append(num_words)
    metadata['last_word'].append(last_word)
    return metadata


def convert_to_mne_python(data, events, event_id, electrode_info, metadata, sfreq_data, tmin, tmax):
    '''

    :param data:
    :param events:
    :param event_id:
    :param electrode_labels:
    :param metadata:
    :param sfreq_data:
    :param tmin:
    :param tmax:
    :return:
    '''
    channel_names = [s[0][0]+'-'+s[3][0] for s in electrode_info['labels']]
    regions = set([s[3][0] for s in electrode_info['labels']])
    print('Regions: ' + ' '.join(regions))
    montage = mne.channels.Montage(electrode_info['coordinates'], channel_names, 'misc', range(len(channel_names)))
    # fig_montage = montage.plot(kind='3d')
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    info = mne.create_info(ch_names=channel_names, sfreq=sfreq_data, ch_types=ch_types)#, montage=montage)
    raw = mne.io.RawArray(data, info)

    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, metadata=metadata, baseline=None,
                        preload=False)
    return info, epochs



def create_events_array(metadata):
    '''

    :param metadata: (pandas dataframe) num_words X num_features; all words across all stimuli
    :param params: (object) general parameters
    :return:
    '''

    # First column of events object
    curr_times = np.expand_dims(metadata['event_time'].values, axis=1)

    # Second column
    second_column = np.zeros((len(curr_times), 1))

    # Third column
    event_numbers = range(len(curr_times))  # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
    event_numbers = np.expand_dims(event_numbers, axis=1)

    # EVENT object: concatenate all three columns together (then change to int and sort)
    events = np.hstack((curr_times, second_column, event_numbers))
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    # EVENT_ID dictionary: mapping block names to event numbers
    event_id = dict([(str(event_type_name), event_number[0]) for event_type_name, event_number in zip(event_numbers, event_numbers)])


    return events, event_id
