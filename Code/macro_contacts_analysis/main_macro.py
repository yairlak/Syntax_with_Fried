import numpy as np
import os, glob
import neo, mne
from neo.io import BlackrockIO
import matplotlib.pyplot as plt
import scipy

class settings:
    def __init__(self):
        self.hospital = 'UCLA'
        self.patient = 'patient_479'
        self.path2data = os.path.join('..', 'Data', self.hospital, self.patient)
        self.files = glob.glob(os.path.join(self.path2data, 'CSC*.mat'))
        self.log_prefix = 'new_mouse_recording_in_cheetah_clock'
class params:
    def __init__(self):
        self.sfreq = 2000 # Data sampling frequency [Hz]
        self.line_frequency = 60  # Line frequency [Hz]
        self.tmin = -2  # Start time before event [sec]
        self.tmax = 2 # End time after event [sec]

def load_data(settings):
    num_files = len(settings.files)
    for f, mat_file in enumerate(settings.files):
        curr_cluster = scipy.io.loadmat(mat_file)
        # initialize data array on the first file
        if f == 0:
            data_all_channels = np.empty([4, len(curr_cluster['data'][0])])
        if f>11 and f<15:
            data_all_channels[f-11,:] = curr_cluster['data'][0]
    return data_all_channels

def get_TTLs(settings):
    log_files = glob.glob(os.path(settings.path2data, settings.log_prefix + '*.log'))
    for cnt_f, curr_log_file in enumerate(log_files):
        with open(curr_log_file) as f:
            content = f.readlines()
        #TTLs_subset = events[np.argwhere(events[:,2] == 60), 0]
    #plt.scatter(TTLs, np.ones(len(TTLs)))
    #plt.scatter(TTLs_subset, np.ones(len(TTLs_subset)), edgecolors = 'r')
    #plt.show

    return events

def update_counters(cnt_word_items, cnt_type, trial, cnt_block):
    cnt_type += 1  # forward the type counter
    cnt_type = cnt_type % 3  # Make sure it is 3-cyclic
    cnt_word_items = 1  # Start counting the token items from 1
    if cnt_type == 0: # If elliptic finished, and back to fixation then change the trial number
        trial += 1
        if trial == 40:  # If last trial (assuming always 40 trials in each block) then increase block number
            trial = 0
            cnt_block += 1
    return cnt_word_items, cnt_type, trial, cnt_block

def generate_mne_raw_object(data_all_channels, params):
    num_channels = data_all_channels.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=ch_names, sfreq=params.sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(data_all_channels, info)
    return raw


# ---------------------- MAIN SCRIPT ---------------------------------

# Load settings (path, file names, etc.)
settings = settings()

# Load parameters (sampling rate, etc.)
params = params()

# Get TTLs from last channel and generate events mne-object
print('Collecting TTLs...')
events = get_TTLs(settings)

# Load data (BlackRock, Neuralynx, etc.)
print('Loading data...')
data_all_channels = load_data(settings)

# Average referencing of the data
print('Referencing (average) the data...')
#data_all_channels = data_all_channels - np.mean(data_all_channels, axis=1)

# Z-scoring the data
print('z-score transform...')
#data_all_channels.nsx_data_ave_ref_zscore = scipy.stats.zscore(data_all_channels.nsx_data_ave_ref, axis=1)

# ---------------------------------------------
# Epoch the data according to a given event_id
event_ids = [30, 60, 130, 160, 230, 260]  # Choose Block, type and word item to lock to
event_ids = [60]

# List of freq bands
#iter_freqs = [('Theta', 4, 7),('Alpha', 8, 12),('Beta', 13, 25),('Gamma', 30, 45), ('High-Gamma', 70, 150)]
iter_freqs = [('High-Gamma', 70, 150)]
fstep = 2 # [Hz] Step in spectrogram

# Convert data to mne raw
print('Generating MNE raw object...')
raw = generate_mne_raw_object(data_all_channels, params)
raw.set_eeg_reference('average', projection=False)  # set EEG average reference
raw.plot()
raw.notch_filter(params.line_frequency, fir_design='firwin')


for channel in range(128):
    file_name = 'ERP_Patient_' + settings.hospital + settings.patient + settings.file_stem + \
                '_Channel_' + str(channel + 1) + \
                '_Event_id' + str(event_id) + '.png'
    epochs.plot_image(picks=channel, show = False)
    fig = plt.gcf()
    fig.savefig(os.path.join('..', 'Figures', 'ERPs', file_name))
    plt.close(fig)

    file_name = 'Spec_Patient_' + settings.hospital + settings.patient + settings.file_stem + \
                '_Channel_' + str(channel + 1) + \
                '_Event_id' + str(event_id) + '.png'
    epochs.plot_psd(picks=[channel], show = False)
    fig = plt.gcf()
    fig.savefig(os.path.join('..', 'Figures', 'PSDs', file_name))
    plt.close(fig)

    freqs = np.arange(fmin, fmax, fstep)
    n_cycles = freqs / 2
    file_name = 'ERF_Patient_' + settings.hospital + settings.patient + settings.file_stem + \
                '_Channel_' + str(channel + 1) + \
                '_Event_id' + str(event_id) + '.png'
    power = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, average=False, n_cycles=n_cycles, return_itc=False, picks = [channel])
    power_ave = np.squeeze(np.average(power.data, axis=2))
    fig, ax = plt.subplots(figsize=(6, 6))
    map = ax.imshow(power_ave, extent=[np.min(power.times), np.max(power.times), 1, 40], interpolation='nearest', aspect='auto')
    plt.colorbar(map, label = 'Power')
    fig.savefig(os.path.join('..', 'Figures', 'ERFs', file_name))
    plt.close(fig)