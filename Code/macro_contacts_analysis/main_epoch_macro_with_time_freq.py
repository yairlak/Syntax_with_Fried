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

class settings:
    def __init__(self):
        self.patient = 'patient_479'
        self.file_stem = 'patient_479'
        self.blocks = [1, 3, 5]
        settings.blocks_str = ''.join(str(x) for x in self.blocks)
        self.log_name_beginning = 'new_mouse_recording_in_cheetah_clock_part'
        self.path2log = os.path.join('..', '..', 'Data', 'UCLA', self.patient)
        self.path2data = os.path.join('..', '..', 'Data', 'UCLA', self.patient, 'ChannelsCSC')
        # self.path2data = os.path.join('..', '..', 'Data', 'UCLA', self.file_stem, 'ChannelsCSC')
        self.path2stimuli = os.path.join('..', '..', 'Paradigm')
        self.stimuli_file = 'features En_02 sentences.xlsx'
        self.time0 = 1489760586848367 # From Ariel CSC files

class params:
    def __init__(self):
        self.sfreq = 30000 # Data sampling frequency [Hz]
        self.line_frequency = [60, 120, 180]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec]
        self.tmax = 3 # End time after event [sec]
        self.time_step = self.tmax * self.sfreq # Epoch into subsequent segments\
        self.downsampling_sfreq = 2000
        self.slice_size = 500 * self.sfreq

class log_object:
    def __init__(self, settings, block):
        self.log_filename = settings.log_name_beginning + str(block) + '.log'

    def append_log(self):
        with open(os.path.join(settings.path2data, self.log_filename)) as f:
            self.log_content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            self.log_content = [x.strip() for x in self.log_content]

    def read_and_parse_log(self, settings):
        with open(os.path.join(settings.path2log, self.log_filename)) as f:
            log_content = [line.split() for line in f]

        # Find all event types (DISPLAY_TEXT, FIXATION, KEY_PRESS, etc.)
        event_types = [i[1] for i in log_content]
        event_types = list(set().union(event_types, event_types))

        # For each event type, extract onset times and stimulus information
        event_types_added = []
        for event_type in event_types:
            if event_type == 'DISPLAY_TEXT':
                setattr(self, event_type + '_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_TIMES')
                setattr(self, event_type + '_ON_TOKEN_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_TOKEN_NUM')
                setattr(self, event_type + '_ON_SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_SENTENCE_NUM')
                setattr(self, event_type + '_ON_WORD_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_WORD_NUM')
                setattr(self, event_type + '_ON_WORD', [i[5] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_WORD')
                setattr(self, 'FIRST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF' if i[4] == '1'])
                event_types_added.append('FIRST_WORD_TIMES')

                # WORD-IMAGE IS 'OFF':
                setattr(self, event_type + '_OFF_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'OFF'])
                event_types_added.append(event_type + '_OFF_TIMES')

            elif event_type == 'AUDIO_PLAYBACK_ONSET':
                setattr(self, event_type + '_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_TIMES')
                setattr(self, event_type + '_ON_TOKEN_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_TOKEN_NUM')
                setattr(self, event_type + '_ON_SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_SENTENCE_NUM')
                setattr(self, event_type + '_ON_WORD', [i[4] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_WORD')

            elif event_type == 'KEY_PRESS':
                setattr(self, event_type + '_SPACE_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'space'])
                event_types_added.append(event_type + '_SPACE_TIMES')
                setattr(self, event_type + '_l_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'l'])
                event_types_added.append(event_type + '_l_TIMES')
            else:
                setattr(self, event_type + '_TIMES', [i[0] for i in log_content if event_type == i[1]])
                event_types_added.append(event_type + '_TIMES')

        setattr(self, 'event_types', event_types_added)

        return self


def generate_events_array(log_all_blocks, settings, params):
    # Initialize arrays
    events = np.empty((0, 3))
    event_id = dict()

    for block, log in enumerate(log_all_blocks):
        block_number = settings.blocks[block]
        # Add all event times from log to events object.
        relevant_event_types = ['FIRST_WORD_TIMES', 'KEY_PRESS_l_TIMES']
        corresponding_event_numbers = [1, 2]

        for i, event_type in enumerate(relevant_event_types):
            event_number = corresponding_event_numbers[i] + 20 * (block_number - 1) # For each block, the event_ids are ordered within a range of 20 number 1-20, 21-40, etc.
            event_type_name = event_type + '_block_' + str(block_number)
            event_id[event_type_name] = event_number
            curr_times = getattr(log, event_type)
            curr_times = np.asarray(curr_times, dtype=float)
            curr_times = params.sfreq * (curr_times - settings.time0)/1e6 # Subtract the beginning of the recording and convert to samples
            curr_times = np.expand_dims(curr_times, axis=1)

            num_events = len(curr_times)
            second_column = np.zeros((num_events, 1))
            third_column = event_number * np.ones((num_events, 1))
            curr_array = np.hstack((curr_times, second_column, third_column))

            events = np.vstack((events, curr_array))

    # Change to integer and sort events object
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    return events, event_id


def load_data(settings):
    CSC_file = glob.glob(os.path.join(settings.path2data, 'CSC' + str(settings.channel) + '.mat'))
    data_all = io.loadmat(CSC_file[0])['data']
    settings.channel_name = scipy.io.loadmat(CSC_file[0])['file_name'][0]
    return data_all, settings


def get_TTLs(settings):
    fn = os.path.join('..', '..', 'Output', 'raw_data_with_events_to_python_all_comparisons_' + settings.patient + '_sentences_blocks_' + settings.blocks_str + '.mat')
    print fn
    data_events = scipy.io.loadmat(fn) # These are in msec
    return data_events


def generate_mne_raw_object(data, params):
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=ch_names, sfreq=params.sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    return raw

# --------------------------------------
# ------------ START MAIN --------------
# --------------------------------------
# Load settings (path, file names, etc.)
settings = settings()

# Load parameters (sampling rate, etc.)
params = params()

# Read log file (add line: log.append_log() to append the entire log to the object)
log_all_blocks = []
for block in settings.blocks:
    log = log_object(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))

# IF RUNNING FROM A BASH SCRIPT !!!!!
print sys.argv[1]
channel = int(sys.argv[1])
# -------------------------
# channel = 21
for channel in range(channel, channel+10):
    settings.channel = channel
    # Load CSC mat files from CSC folder
    print('Loading data...')
    data_all, settings = load_data(settings)
    # Load event times from Output folder
    print('Load events...')
    data_events = get_TTLs(settings)
    events = data_events['custom_events_all_comparisons']
    event_ids = data_events['event_id_all_comparisons']



    print('Generating MNE raw object...')
    raw = generate_mne_raw_object(data_all, params)

    for comparison, events in enumerate(data_events['custom_events_all_comparisons'][0]):
        print(comparison)
        curr_comparison_name = data_events['comparison_name'][0, comparison][0]
        # TEMP !!!!!!!!!!!!
        curr_comparison_name = 'ALL'
        # ---------------------

        # Create Events object for MNE
        event_id_temp = data_events['event_id_all_comparisons'][0, comparison][0]
        event_id_temp = [['FIRST_WORD_TIMES'], ['KEY_PRESS_l_TIMES']]
        event_id = {}
        for x, id in enumerate(event_id_temp):
            event_id[id[0]] = x
        events = events.astype(int)
        sort_IX = np.argsort(events[:, 0], axis=0)
        events = events[sort_IX, :]
        events[:, 0] = events[:, 0] * params.sfreq/1000 # from msec to samples

        # TEMP !!!!!!!!!!!!
        events, event_id = generate_events_array(log_all_blocks, settings, params)
        #------------------------------

        # Create Epochs object
        # picks = range(0, 2)
        # decim = 20  # decimate to make faster to run
        print('Epoching data...')
        epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)
        print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
        epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
        print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')
        del epochs

        iter_freqs = [('High-Gamma', 70, 150)]
        fstep = 2  # [Hz] Step in spectrogram

        event_ids_epochs = epochs_resampled.event_id.keys()

        for band, fmin, fmax in iter_freqs:
            file_name = band + '_Patient_' + settings.file_stem + '_Channel_' + str(channel + 1) + '_Event_id' + str(
                epochs_resampled.event_id.values()) + settings.channel_name + '.png'
            freqs = np.arange(fmin, fmax, fstep)
            n_cycles = freqs / 2
            print('Time-freq...')
            event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
            power1 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_1], freqs=freqs, n_jobs=30, average=False, n_cycles=n_cycles,
                                                  return_itc=False, picks=[0])

            event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
            power2 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_2], freqs=freqs, n_jobs=30, average=False,
                                                   n_cycles=n_cycles,
                                                   return_itc=False, picks=[0])

            power_ave1 = np.squeeze(np.average(power1.data, axis=2))
            power_ave2 = np.squeeze(np.average(power2.data, axis=2))

            fig, axs = plt.subplots(2, 1, figsize=(6, 6))
            cnt = 0
            for ax in axs.reshape(-1):
                if cnt == 0:
                    vmax1 = np.mean(power_ave1) + 1 * np.std(power_ave1)
                    map = ax.imshow(power_ave1, extent=[np.min(power1.times), np.max(power1.times), 1, power1.data.shape[0] + 1],
                                interpolation='nearest',
                                aspect='auto', vmin=0, vmax=vmax1)
                    plt.colorbar(map, ax=ax, label='Power')
                    ax.set_title(event_id_temp[0][0])
                    ax.set_ylabel('Trial')
                elif cnt ==1:
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

            fig.savefig(os.path.join('..', '..', 'Figures', 'HighGamma', file_name))
            plt.close(fig)
