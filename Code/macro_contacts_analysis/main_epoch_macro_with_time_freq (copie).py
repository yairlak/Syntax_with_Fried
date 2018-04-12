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
	settings.patient ='patient_479'
        settings.file_stem = 'patient_479'
        self.path2data = os.path.join('..', '..', 'Data', 'UCLA', 'patient_479', 'ChannelsCSC')
        blocks = range(1,7,1)
        settings.blocks_str = ''.join(str(x) for x in blocks)

class params:
    def __init__(self):
        self.sfreq = 30000 # Data sampling frequency [Hz]
        self.line_frequency = [60, 120, 180]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec]
        self.tmax = 3 # End time after event [sec]
        self.time_step = self.tmax * self.sfreq # Epoch into subsequent segments\
        self.downsampling_sfreq = 2000
        self.slice_size = 500 * self.sfreq

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

print sys.argv[1]
channel = int(sys.argv[1])
# Load settings (path, file names, etc.)
settings = settings()
# Load parameters (sampling rate, etc.)
params = params()

for channel in range(channel, channel+5):
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

        # Create Events object for MNE
        event_id_temp = data_events['event_id_all_comparisons'][0, comparison][0]
        event_id = {}
        for x, id in enumerate(event_id_temp):
            event_id[id[0]] = x
        events = events.astype(int)
        sort_IX = np.argsort(events[:, 0], axis=0)
        events = events[sort_IX, :]
        events[:, 0] = events[:, 0] * params.sfreq/1000 # from msec to samples

        # Create Epochs object
        # picks = range(0, 2)
        # decim = 20  # decimate to make faster to run
        print('Epoching data...')
        epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
        print(epochs)
        print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
        epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
        print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')

        iter_freqs = [('High-Gamma', 70, 150)]
        fstep = 2  # [Hz] Step in spectrogram

        for band, fmin, fmax in iter_freqs:
            file_name = band + '_Patient_' + settings.file_stem + '_Channel_' + str(channel + 1) + '_Event_id' + str(
                event_id) + settings.channel_name + '.png'
            freqs = np.arange(fmin, fmax, fstep)
            n_cycles = freqs / 2
            print('Time-freq...')
            power1 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_temp[0][0]], freqs=freqs, n_jobs=30, average=False, n_cycles=n_cycles,
                                                  return_itc=False, picks=[0])
            power2 = mne.time_frequency.tfr_morlet(epochs_resampled[event_id_temp[1][0]], freqs=freqs, n_jobs=30, average=False,
                                                   n_cycles=n_cycles,
                                                   return_itc=False, picks=[0])
            power_ave1 = np.squeeze(np.average(power1.data, axis=2))
            power_ave2 = np.squeeze(np.average(power2.data, axis=2))
            fig, axs = plt.subplots(2, 1, figsize=(6, 6))
            cnt = 0
            for ax in axs.reshape(-1):
                if cnt == 0:
                    map = ax.imshow(power_ave1, extent=[np.min(power1.times), np.max(power1.times), 1, power1.data.shape[0] + 1],
                                interpolation='nearest',
                                aspect='auto')
                    plt.colorbar(map, ax=ax, label='Power')
                    ax.set_title(event_id_temp[0][0])
                    ax.set_ylabel('Trial')
                elif cnt ==1:
                    map1 = ax.imshow(power_ave2,
                                    extent=[np.min(power2.times), np.max(power2.times), 1, power2.data.shape[0] + 1],
                                    interpolation='nearest',
                                    aspect='auto')
                    ax.set_title(event_id_temp[1][0])
                    plt.colorbar(map1, ax=ax, label='Power')
                    ax.set_ylabel('Trial')
                    ax.set_xlabel('Time [sec]')
                cnt += 1

            fig.savefig(os.path.join('..', '..', 'Figures', 'HighGamma', file_name))
            plt.close(fig)
