import os, glob
import numpy as np
import mne
from scipy import io

def get_channel_nums(path2rawdata):
    CSC_files = glob.glob(os.path.join(path2rawdata, 'micro', 'CSC_mat', 'CSC?.mat')) + \
                glob.glob(os.path.join(path2rawdata, 'micro', 'CSC_mat', 'CSC??.mat')) + \
                glob.glob(os.path.join(path2rawdata, 'micro', 'CSC_mat', 'CSC???.mat'))
    return [int(os.path.basename(s)[3:-4]) for s in CSC_files]


def get_probes2channels(patient):
    '''
    input: patient (str)
    output: probes (dict) - keys are probe names, values are channel numbers for micro or macro data. For example, probes['LSTG']['micro'] = [25, 26, ...]
    '''
    probes = {}

    path2microdata_folder = os.path.join('..', '..', 'Data', 'UCLA', patient, 'Raw', 'micro', 'CSC_mat')
    path2macrodata_folder = os.path.join('..', '..', 'Data', 'UCLA', patient, 'Raw', 'macro', 'CSC_mat')
    
    # MICRO CSC
    with open(os.path.join(path2microdata_folder, 'channel_numbers_to_names.txt')) as f:
        lines = f.readlines()
    channel_numbers_micro  = [l.strip().split('\t')[0] for l in lines]
    file_names_micro = [l.strip().split('\t')[1] for l in lines]
    probe_names_micro = set([s[4:-5] for s in file_names_micro if s.startswith('G')])
    
    # MACRO CSC
    with open(os.path.join(path2macrodata_folder, 'channel_numbers_to_names.txt')) as f:
        lines = f.readlines()
    channel_numbers_macro = [l.strip().split('\t')[0] for l in lines]
    file_names_macro = [l.strip().split('\t')[1] for l in lines]
    probe_names_macro = set([s[:-5] for s in file_names_macro])

    if not probe_names_micro == probe_names_macro:
        print('--- !!! Warning: not the same probe names in micro and macro !!! ---')
        print('Micro probe names: %s' % probe_names_micro)
        print('Macro probe names: %s' % probe_names_macro)
        

    for probe_name in list(set(probe_names_micro))+list(set(probe_names_macro)): # Take the union in case probe_names_micro != probe_names_macro
        channel_numbers_of_probe_micro = [int(ch) for (ch, fn) in zip(channel_numbers_micro, file_names_micro) if probe_name == fn[4:-5]]
        channel_numbers_of_probe_macro = [int(ch) for (ch, fn) in zip(channel_numbers_micro, file_names_macro) if probe_name == fn[:-5]]
        probes[probe_name] = {}
        probes[probe_name]['micro'] = channel_numbers_of_probe_micro
        probes[probe_name]['macro'] = channel_numbers_of_probe_macro
    # MICROPHPNE to micro electrodes
    probes['MICROPHONE'] = {}
    probes['MICROPHONE']['micro'] = [0]

    return probes

def load_channelsCSC_data(path2rawdata, channel):
    CSC_file = glob.glob(os.path.join(path2rawdata, 'micro', 'CSC_mat', 'CSC' + str(channel) + '.mat'))
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
    CSC_files = glob.glob(os.path.join(path2rawdata, 'macro', 'CSC_mat', 'CSC*.mat'))
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


def load_combinato_sorted_h5(channel_num, channel_name, settings):
    import h5py
    spike_times_msec = []; channel_names = []

    h5_files = glob.glob(os.path.join(settings.path2rawdata, 'micro', 'CSC_ncs' , 'CSC' + str(channel_num), 'data_*.h5'))
    if len(h5_files) == 1:
        filename = h5_files[0]
        f_all_spikes = h5py.File(filename, 'r')

        for sign in ['neg', 'pos']:
        #for sign in ['neg']:
            #filename_sorted = glob.glob(os.path.join(settings.path2rawdata, 'micro', 'CSC_ncs', 'CSC' + str(channel_num), 'sort_' + sign + '_simple', 'sort_cat.h5'))[0]
            filename_sorted = glob.glob(os.path.join(settings.path2rawdata, 'micro', 'CSC_ncs', 'CSC' + str(channel_num), 'sort_' + sign + '_yl2', 'sort_cat.h5'))
            if len(filename_sorted) == 1:
                f_sort_cat = h5py.File(filename_sorted[0], 'r')
                #print('classes', f_sort_cat['classes'].value)
                #print('index', f_sort_cat['index'].value)
                #print('matches', f_sort_cat['matches'].value)
                #print('groups', f_sort_cat['groups'].value)
                #print('types', f_sort_cat['types'].value)
                try:
                    classes =  f_sort_cat['classes'].value
                    index = f_sort_cat['index'].value
                    matches = f_sort_cat['matches'].value
                    groups = f_sort_cat['groups'].value
                    group_numbers = set([g[1] for g in groups])
                    types = f_sort_cat['types'].value # -1: artifact, 0: unassigned, 1: MU, 2: SU

                    # For each group, generate a list with all spike times and append to spike_times
                    for g in list(group_numbers):
                        IXs = []
                        type_of_curr_group = [t_ for (g_, t_) in types if g_ == g]
                        if len(type_of_curr_group) == 1:
                            type_of_curr_group = type_of_curr_group[0]
                        else:
                            raise ('issue with types: more than one group assigned to a type')
                        if type_of_curr_group>0: # ignore artifact and unassigned groups

                            # Loop over all spikes
                            for i, c in enumerate(classes):
                                # check if current cluster in group
                                g_of_curr_cluster = [g_ for (c_, g_) in groups if c_ == c]
                                if len(g_of_curr_cluster) == 1:
                                    g_of_curr_cluster = g_of_curr_cluster[0]
                                else:
                                    raise('issue with groups: more than one group assigned to a cluster')
                                # if curr spike is in a cluster of the current group
                                if g_of_curr_cluster == g:
                                    curr_IX = index[i]
                                    IXs.append(curr_IX)

                            curr_spike_times = f_all_spikes[sign]['times'].value[IXs]
                            spike_times_msec.append(curr_spike_times)
                            region_name = channel_name[1+channel_name.find("-"):channel_name.find(".")]
                            channel_names.append(sign[0] + '_g' + str(g) + '_' + str(channel_num)+ '_' + region_name)
                except:
                    print('Something is wrong with %s, %s' % (sign, filename_sorted[0]))
            else:
                print('%s was not found!' % os.path.join(settings.path2rawdata, 'micro', 'CSC_ncs', 'CSC' + str(channel_num), 'sort_' + sign + '_yl2', 'sort_cat.h5'))

        print(channel_num)

    else:
        print('None or more than a single combinato h5 was found')

    return spike_times_msec, channel_names


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
