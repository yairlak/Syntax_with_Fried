import os, glob
import numpy as np
import mne
from scipy import io
from functions import convert_to_mne

def compute_time_freq(channel_num, channel_name, channel_data, events, event_id, metadata, settings, params):
    print('Analyzing high-gamma for channel ' + str(channel_num))

    print('Generating MNE raw object for continuous data...')
    num_channels = channel_data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    info = mne.create_info(ch_names=[settings.channel_name], sfreq=params.sfreq_raw, ch_types=ch_types)
    raw = mne.io.RawArray(channel_data, info)

    print('Line filtering...')
    raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

    print('Epoching data...')
    epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None, preload=True)
    print(epochs)

    print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
    epochs.resample(params.downsampling_sfreq, npad='auto')
    print('New sampling rate:', epochs.info['sfreq'], 'Hz')

    del raw, channel_data

    print('Time-frequency analyses...')
    band, fmin, fmax = params.iter_freqs[0]
    print('Band: ' + band)
    epochsTFR = average_high_gamma(epochs, band, fmin, fmax, params.freq_step, [], 'no_baseline', params)
    epochsTFR.metadata = metadata

    return epochsTFR


def average_high_gamma(epochs, band, fmin, fmax, fstep, baseline, baseline_type, params):
    freqs = np.arange(fmin, fmax, fstep)
    # -------------------------------
    # - delta_F =  2 * F / n_cycles -
    # - delta_T = n_cycles / F / pi -
    # - delta_T * delta_F = 2 / pi  -
    # -------------------------------
    # n_cycles = freq[0] / freqs * 3.14
    # n_cycles = freqs / 2.
    n_cycles = 7 # Fieldtrip's default
    if band == 'High-Gamma': n_cycles = 20

    power = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, n_jobs=-2, average=False, n_cycles=n_cycles,
                                          return_itc=False, picks=[0])
    # power_ave = np.squeeze(np.average(power.data, axis=2))

    return power