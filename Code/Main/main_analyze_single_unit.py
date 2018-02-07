from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, analyses
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------
# ------------ START MAIN --------------
# --------------------------------------

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# -----------------------------------
# --------- LOAD DATA & LOGS --------
# -----------------------------------
print('Loading settings...')
settings = load_settings_params.Settings()

print('Loading parameters...')
params = load_settings_params.Params()

print('Loading CSC raw data...')
raw_CSC_data_in_mat, settings = load_data.raw_in_matlab_format(settings)

print('Loading spike sorted data (spike clusters)...')
spikes, settings, electrode_names, electrode_names_from_raw_files = load_data.spike_clusters(settings)
settings.time0 = 1.489760586848367e+15
settings.timeend = settings.timeend + settings.time0

print('Reading log file from experiment...')
log_all_blocks = []
for block in settings.blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))

# -----------------------------------
# ------- Generate MNE objects ------
# -----------------------------------
print('Generating event object for MNE from log data...')
events, events_spikes, event_id = read_logs_and_comparisons.generate_events_array(log_all_blocks, settings, params)

print('Generating MNE raw object for spikes...')
settings.time0 = 0
settings.timeend = 3.159231975000000e+09
raw_spikes = load_data.generate_mne_raw_object_for_spikes(spikes, electrode_names_from_raw_files, settings, params)

print('Epoching spiking data...')
epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, baseline=None, preload=True)
print(epochs_spikes)

# Plot the events to get an idea of the paradigm
color = {1: 'green', 41: 'yellow', 81: 'red', 2: 'c', 42: 'black', 82: 'blue'}
fig_paradigm = mne.viz.plot_events(events_spikes, raw_spikes.info['sfreq'], raw_spikes.first_samp, color=color,
                    event_id=event_id, show=False)
fname = 'paradigm_events_' + settings.hospital + '_' + settings.patient + '.png'
plt.savefig(os.path.join(settings.path2figures, 'misc', fname))

print('Loading electrode names for all channels...')
electrode_names = load_data.electrodes_names(settings)

file_name_epochs = settings.hospital + '_' + settings.patient + 'line_filtered_resampled-epo.fif'

if not settings.load_line_filtered_resampled_epoch_object:
    print('Generating MNE raw object for continuous data...')
    raw = load_data.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

    print('Line filtering...')
    raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

    print('Epoching data...')
    epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, baseline=None, preload=True)
    print(epochs)

    print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
    epochs_resampled = epochs.copy().resample(params.downsampling_sfreq, npad='auto')
    print('New sampling rate:', epochs_resampled.info['sfreq'], 'Hz')

    print('Save Epoch data after line filtering and resampling')
    epochs_resampled.save(os.path.join(settings.path2epoch_data, file_name_epochs))
else:
    print('Loading already epoch data, after line filtering and resampling')
    epochs_resampled = mne.read_epochs(os.path.join(settings.path2epoch_data, file_name_epochs))


# -----------------------------------
# --------- Start ANALYSES ----------
# -----------------------------------
print('Generate rasters and PSTHs...')
# analyses.generate_rasters(epochs_spikes, settings)

print('High-Gamma analyses...')
event_ids_epochs = epochs_resampled.event_id.keys()
for band, fmin, fmax in params.iter_freqs:
    # Calculate average power activity
    event_id_1 = [s for s in event_ids_epochs if "FIRST_WORD" in s]
    power1, power_ave1 = analyses.average_high_gamma(epochs_resampled, event_id_1, band, fmin, fmax, params.freq_step)
    event_id_2 = [s for s in event_ids_epochs if "KEY" in s]
    power2, power_ave2 = analyses.average_high_gamma(epochs_resampled, event_id_2, band, fmin, fmax, params.freq_step)
    # PLOT
    file_name = band + '_' + settings.patient + '_Channel_' + str(settings.channel + 1) + '_Event_id' + str(
        epochs_resampled.event_id.values()) + settings.channel_name + '.png'
    analyses.plot_and_save_average_freq_band(power1, power2, power_ave1, power_ave2, event_id_1, event_id_2, file_name)