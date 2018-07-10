import numpy as np

def smooth_with_gaussian(time_series, sfreq, gaussian_width = 50, N=1000):
    # gaussian_width in samples
    # ---------------------
    import math
    from scipy import signal
    norm_factor = np.sqrt(2 * math.pi * gaussian_width ** 2)/sfreq # sanity check: norm_factor = gaussian_window.sum()
    gaussian_window = signal.general_gaussian(M=N, p=1, sig=gaussian_width) # generate gaussian filter
    norm_factor = (gaussian_window/sfreq).sum()
    smoothed_time_series = np.convolve(time_series, gaussian_window/norm_factor, mode="full") # smooth
    smoothed_time_series = smoothed_time_series[int(round(N/2)):-(int(round(N/2))-1)] # trim ends
    return smoothed_time_series
