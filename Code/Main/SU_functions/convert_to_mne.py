import os
import numpy as np
import mne


def generate_events_array(log_all_blocks, comparison, word2pos, settings, params, preferences):
    # Initialize arrays
    events = np.empty((0, 3))
    event_id = dict()

    for block, log in enumerate(log_all_blocks):
        block_number = settings.blocks[block]
        # Add all event times from log to events object.
        if not preferences.run_contrasts:
            if preferences.run_POS:
                # First reduce the number of classes by lumping together fine syntactic cagtegories into a single categ
                simpler_syn_categories = ['NN', 'VB', 'PRP', 'WP', 'JJ', 'RB', 'DT', 'IN', 'MD']
                syntactic_categories_simpler = {}
                for word, categ in word2pos.items():
                    for simpler_syn_categ in simpler_syn_categories:
                        if simpler_syn_categ in categ:
                            syntactic_categories_simpler[word] = simpler_syn_categ
                            break

                # Extract word_onset times for each syntactic category
                for i, syn_categ in enumerate(simpler_syn_categories):
                    event_number = i + 100 * (block_number)  # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
                    event_type_name = syn_categ + '_block_' + str(block_number)
                    event_id[event_type_name] = event_number
                    curr_times = getattr(log, 'WORDS_ON_TIMES')
                    curr_times = np.asarray(curr_times, dtype=float)
                    curr_times = params.sfreq_raw * (curr_times - settings.time0) / 1e6  # Subtract the beginning of the recording and convert to samples
                    curr_times = np.expand_dims(curr_times, axis=1)

                    words = [w[0:-1].lower() if w[-1] == '?' or w[-1] == '.' else w.lower() for w in getattr(log, 'WORD_STRING')]
                    IX_curr_syn_categ = [j for j, w in enumerate(words) if syntactic_categories_simpler[w] == syn_categ]
                    curr_times = curr_times[IX_curr_syn_categ]

                    num_events = len(curr_times)
                    second_column = np.zeros((num_events, 1))
                    third_column = event_number * np.ones((num_events, 1))
                    curr_array = np.hstack((curr_times, second_column, third_column))

                    events = np.vstack((events, curr_array))

                    curr_times = None; second_column = None; third_column = None; curr_array = None

            else:
                for i, event_type in enumerate(settings.event_types_to_extract):
                    if hasattr(log, event_type):
                        event_number = settings.event_numbers_to_assign_to_extracted_event_types[i] + 100 * (block_number) # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
                        event_type_name = event_type + '_block_' + str(block_number)
                        event_id[event_type_name] = event_number
                        curr_times = getattr(log, event_type)
                        curr_times = np.asarray(curr_times, dtype=float)
                        curr_times = params.sfreq_raw * (curr_times - settings.time0)/1e6 # Subtract the beginning of the recording and convert to samples
                        curr_times = np.expand_dims(curr_times, axis=1)

                        num_events = len(curr_times)
                        second_column = np.zeros((num_events, 1))
                        third_column = event_number * np.ones((num_events, 1))
                        curr_array = np.hstack((curr_times, second_column, third_column))

                        events = np.vstack((events, curr_array))

                    curr_times = None; second_column = None; third_column = None; curr_array = None
        else: # Run contrasts
            for j, cond in enumerate(comparison[0]):
                # if hasattr(log, event_type): # Assumes LAST_WORD
                event_number = j + 100 * (block_number)  # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
                event_type_name = comparison[1] + '_' + str(j) + '_block_' + str(block_number)
                event_id[event_type_name] = event_number
                align_to = comparison[1] # FIRST_WORD_TIMES or LAST_WORD_TIMES
                curr_times = getattr(log, align_to)
                curr_times = np.asarray(curr_times, dtype=float)
                IX_contrast_sentences = [IX-1 for IX in log.SENTENCE_NUM_ORDER if IX in cond['trial_numbers']]
                curr_times = curr_times[IX_contrast_sentences]
                curr_times = params.sfreq_raw * (curr_times - settings.time0) / 1e6  # Subtract the beginning of the recording and convert to samples
                curr_times = np.expand_dims(curr_times, axis=1)

                num_events = len(curr_times)
                second_column = np.zeros((num_events, 1))
                third_column = event_number * np.ones((num_events, 1))
                curr_array = np.hstack((curr_times, second_column, third_column))

                events = np.vstack((events, curr_array))

                curr_times = None; second_column = None; third_column = None; curr_array = None

    # Change to integer and sort events object
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    events_spikes = np.copy(events)
    events_spikes[:, 0] = events_spikes[:, 0] * params.sfreq_spikes / params.sfreq_raw
    events_spikes = events_spikes.astype(np.int64)

    return events, events_spikes, event_id

def generate_mne_raw_object(data, settings, params):
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    # ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=[settings.channel_name], sfreq=params.sfreq_raw, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    return raw

def generate_mne_raw_object_for_spikes(spikes, electrode_names, settings, params):
    sfreq = params.sfreq_spikes
    num_channels = len(spikes)
    ch_types = ['seeg' for s in range(num_channels)]
    #ch_names = ['sEEG_%s' % s for s in range(num_channels)]
    info = mne.create_info(ch_names=electrode_names, sfreq=sfreq, ch_types=ch_types)

    num_samples = 1+int(sfreq * (settings.timeend - settings.time0)/1e6) # Use same sampling rate as for macro, just for convenience.
    spikes_matrix_all_clusters = np.empty((0, num_samples))
    for cluster, curr_spike_times in enumerate(spikes):
        spikes_zero_one_vec = np.zeros(num_samples) # convert to samples from sec
        curr_spike_times = (curr_spike_times - settings.time0 / 1e6) * sfreq # convert to samples from sec
        curr_spike_times = curr_spike_times.astype(np.int64)
        spikes_zero_one_vec[curr_spike_times] = 1
        spikes_matrix_all_clusters = np.vstack((spikes_matrix_all_clusters, spikes_zero_one_vec))
    raw = mne.io.RawArray(spikes_matrix_all_clusters, info)
    return raw
