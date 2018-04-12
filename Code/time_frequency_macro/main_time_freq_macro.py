import numpy as np
import os
import neo
from neo.io import BlackrockIO
import mne
import matplotlib.pyplot as plt
import scipy
import glob

class settings:
    def __init__(self):
        settings.file_stem = 'patient_479'
        self.path2data = os.path.join('..', '..', 'Data', 'UCLA', 'patient_479', 'ChannelsCSC')

class params:
    def __init__(self):
        self.sfreq = 40000 # Data sampling frequency [Hz]
        self.line_frequency = [60, 120, 180]  # Line frequency [Hz]
        self.tmin = 0  # Start time before event [sec]
        self.tmax = 60 # End time after event [sec]
        self.time_step = self.tmax * self.sfreq # Epoch into subsequent segments\
        self.downsampling_sfreq = 2000
        self.slice_size = 500 * self.sfreq

def load_data(settings):
    CSC_file = glob.glob(os.path.join(settings.path2data, 'CSC' + str(settings.channel) + '.mat'))
    data_all = scipy.io.loadmat(CSC_file[0])['data']
    settings.channel_name = scipy.io.loadmat(CSC_file[0])['file_name'][0]
    return data_all, settings
    #data_all = []
    #for CSC_file in CSC_files:
    #    x = scipy.io.loadmat(CSC_file)['data']
    #    data_all.append(x)
    #data_all = np.array(data_all)
    #data_all = np.squeeze(data_all, axis=1)

def get_TTLs(data, params):
    event_times = range(0, data.shape[1], params.time_step)
    events = np.zeros([len(event_times), 3], dtype='int32')
    events[:, 0] = event_times
    events[:, 2] = 1
    return events


def generate_mne_raw_object(data, params):
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=ch_names, sfreq=params.sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    return raw

# Load settings (path, file names, etc.)
settings = settings()
# Load parameters (sampling rate, etc.)
params = params()

for channel in range(8,130):
    settings.channel = channel + 1
    # Load data (BlackRock, Neuralynx, from Matlab file, etc.)
    print('Loading data...')
    data_all, settings = load_data(settings)
    print('Generating MNE raw object...')
    raw = generate_mne_raw_object(data_all, params)
    #scalings = 'auto'  # Could also pass a dictionary with some value == 'auto'
    #raw.plot(scalings=scalings, show=True, block=True)#, lowpass=0.1)
    #print('Line filtering of raw object...')
    #raw.notch_filter(params.line_frequency, fir_design='firwin')
    print('Generating TTLs...')
    events = get_TTLs(data_all, params)
    print('Epoching data...')
    event_id = 1
    epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
    print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
    epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
    print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')

    iter_freqs = [('High-Gamma', 70, 150)]
    fstep = 2 # [Hz] Step in spectrogram

    for band, fmin, fmax in iter_freqs:
        # remove evoked response and get analytic signal (envelope)
        file_name = 'ERP_Patient_' + settings.file_stem + '_Channel_' + str(channel + 1)\
                    + '_' + settings.channel_name + '_Event_id_' + str(event_id) + '.png'
        print('ERP...')
        epochs_resampled.plot_image(show = False, picks=[0])
        fig = plt.gcf()
        fig.savefig(os.path.join('..', '..', 'Figures', file_name))
        plt.close(fig)


        file_name = band + '_Patient_' + settings.file_stem + '_Channel_' + str(channel + 1)\
                    + '_' + settings.channel_name + '_Event_id' + str(event_id) + '.png'
        freqs = np.arange(fmin, fmax, fstep)
        n_cycles = freqs/2
        print('Time-freq...')
        power = mne.time_frequency.tfr_morlet(epochs_resampled, freqs=freqs, average=False, n_cycles=n_cycles, return_itc=False, picks=[0])
        power_ave = np.squeeze(np.average(power.data, axis=2))
        fig, ax = plt.subplots(figsize=(6, 6))
        map = ax.imshow(power_ave, extent=[np.min(power.times), np.max(power.times), 1, power.data.shape[0] + 1], interpolation='nearest',
                        aspect='auto')
        plt.colorbar(map, label='Power')
        fig.savefig(os.path.join('..', '..', 'Figures', file_name))
        plt.close(fig)