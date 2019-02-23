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

    if comparison['align_to'] == 'FIRST':
        str_align = 'word_position == 1'
    elif comparison['align_to'] == 'LAST':
        str_align = 'word_position == sentence_length'
    elif comparison['align_to'] == 'END':
        str_align = 'word_position == -1'
    elif comparison['align_to'] == 'EACH':
        str_align = 'word_position > 0'

    queries = []
    for query_cond, label_cond in zip(comparison['query'], comparison['cond_labels']):
        # If pos in query then add double quotes (") around value, e.g. (pos==VB --> pos =="VB")
        new_query_cond = ''
        i = 0
        while i < len(query_cond):
            if query_cond[i:i + len('pos==')] == 'pos==':
                reminder = query_cond[i + len('pos==')::]
                temp_list = reminder.split(" ", 1)
                new_query_cond = new_query_cond + 'pos=="' + temp_list[0] + '" '
                i = i + 6 + len(temp_list[0])
            else:
                new_query_cond += query_cond[i]
                i += 1
            query_cond = new_query_cond

        queries.append(query_cond + ' and ' + str_align + ' and ' + str_blocks)

    return queries
