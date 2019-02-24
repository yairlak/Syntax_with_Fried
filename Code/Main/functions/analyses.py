def compute_time_freq(channel_num, channel_name, channel_data, events, event_id, metadata, settings, params):
    print('Analyzing high-gamma for channel ' + str(channel_num))
    file_name_epochs = 'micro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(channel_num) + '_line_filtered_resampled-epo'

    print('Generating MNE raw object for continuous data...')
    raw = convert_to_mne.generate_mne_raw_object(channel_data, settings, params)

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
    for band, fmin, fmax in params.iter_freqs:
        print('Band: ' + band)
        power, power_ave, _ = average_high_gamma(epochs, band, fmin, fmax, params.freq_step, [], 'no_baseline', params)

    epochs_power = epochs.copy()
    epochs_power.times = power.times
    epochs_power._data = np.expand_dims(power_ave, axis=1)  # To be compatible with MNE functions: add a middle singelton dimenstion for number of channels
    return epochs_power


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
    power_ave = np.squeeze(np.average(power.data, axis=2))
    # Baseline data
    if baseline is None:
        IX = (epochs.times > -abs(params.baseline_period / 1e3)) & (epochs.times < 0) # indices to relevant times
        if baseline_type == 'subtract_average':
            baseline = np.mean(power_ave[:, IX]) # For baseline: Average over negative times (assuming first word alignment)
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
        elif baseline_type == 'trial_wise':
            baseline = np.mean(power_ave[:, IX], axis=1) # For baseline: Average over negative times (assuming first word alignment)
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])

    else:
        if baseline_type == 'subtract_average':
            power_ave_baselined = 10 * np.log10(power_ave / baseline)
            print("Baseline: subtract average")
        elif baseline_type == 'trial_wise':
            power_ave_baselined = 10 * np.log10(power_ave / baseline[:, None])
            print("Baseline: trial-wise")
        elif baseline_type == 'no_baseline':
            power_ave_baselined = power_ave  # don't apply any baseline

    # Gaussian smooth of time-freq results if chosen:
    if params.smooth_time_freq > 0:
        power_ave_baselined_smoothed = np.empty(power_ave_baselined.shape)
        for i in range(power_ave_baselined.shape[0]):
            power_ave_baselined_smoothed[i, :] = smooth_with_gaussian(power_ave_baselined[i, :], params.smooth_time_freq)
    else:
        power_ave_baselined_smoothed = power_ave_baselined

    return power, power_ave_baselined_smoothed, baseline