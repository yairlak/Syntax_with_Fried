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


def get_queries(comparison):
    str_blocks = ['block == {} or '.format(block) for block in eval(comparison['blocks'])]
    str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
    if comparison['generalize_to_modality'] and comparison['generalize_to_contrast']:
        str_blocks_generalize_to = ['block == {} or '.format(block) for block in eval(comparison['generalize_to_modality'])]
        str_blocks_generalize_to = '(' + ''.join(str_blocks_generalize_to)[0:-4] + ')'

    if comparison['align_to'] == 'FIRST':
        str_align = 'word_position == 1'
    elif comparison['align_to'] == 'LAST':
        str_align = 'word_position == sentence_length'
    elif comparison['align_to'] == 'END':
        str_align = 'word_position == -1'
    elif comparison['align_to'] == 'EACH':
        str_align = 'word_position > 0'

    queries = []; queries_generalize_to = []
    for query_cond, label_cond in zip(comparison['query'], comparison['cond_labels']):
        queries.append(query_cond + ' and ' + str_align + ' and ' + str_blocks)
        if comparison['generalize_to_modality'] and comparison['generalize_to_contrast']:
            queries_generalize_to.append(query_cond + ' and ' + str_align + ' and ' + str_blocks_generalize_to)

    return queries, queries_generalize_to