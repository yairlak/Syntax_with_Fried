import os
import numpy as np

class LogSingleUnit:
    def __init__(self, settings, block):
        self.log_filename = settings.log_name_beginning + str(block) + '.log'

    def append_log(self):
        with open(os.path.join(settings.path2data, self.log_filename)) as f:
            self.log_content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            self.log_content = [x.strip() for x in self.log_content]

    def read_and_parse_log(self, settings):
        with open(os.path.join(settings.path2log, self.log_filename)) as f:
            log_content = [line.split() for line in f]

        # Find all event types (DISPLAY_TEXT, FIXATION, KEY_PRESS, etc.)
        event_types = [i[1] for i in log_content]
        event_types = list(set().union(event_types, event_types))

        # For each event type, extract onset times and stimulus information
        event_types_added = []
        for event_type in event_types:
            if event_type == 'DISPLAY_TEXT':
                setattr(self, event_type + '_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_TIMES')
                setattr(self, event_type + '_ON_TOKEN_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_TOKEN_NUM')
                setattr(self, event_type + '_ON_SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_SENTENCE_NUM')
                setattr(self, event_type + '_ON_WORD_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_WORD_NUM')
                setattr(self, event_type + '_ON_WORD', [i[5] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_ON_WORD')
                setattr(self, 'FIRST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF' if i[4] == '1'])
                event_types_added.append('FIRST_WORD_TIMES')

                # WORD-IMAGE IS 'OFF':
                setattr(self, event_type + '_OFF_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'OFF'])
                event_types_added.append(event_type + '_OFF_TIMES')

            elif event_type == 'AUDIO_PLAYBACK_ONSET':
                setattr(self, event_type + '_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_TIMES')
                setattr(self, event_type + '_ON_TOKEN_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_TOKEN_NUM')
                setattr(self, event_type + '_ON_SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_SENTENCE_NUM')
                setattr(self, event_type + '_ON_WORD', [i[4] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_ON_WORD')

            elif event_type == 'KEY_PRESS':
                setattr(self, event_type + '_SPACE_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'space'])
                event_types_added.append(event_type + '_SPACE_TIMES')
                setattr(self, event_type + '_l_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'l'])
                event_types_added.append(event_type + '_l_TIMES')
            else:
                setattr(self, event_type + '_TIMES', [i[0] for i in log_content if event_type == i[1]])
                event_types_added.append(event_type + '_TIMES')

        setattr(self, 'event_types', event_types_added)

        return self


def generate_events_array(log_all_blocks, settings, params):
    # Initialize arrays
    events = np.empty((0, 3))
    event_id = dict()

    for block, log in enumerate(log_all_blocks):
        block_number = settings.blocks[block]
        # Add all event times from log to events object.
        relevant_event_types = ['FIRST_WORD_TIMES', 'KEY_PRESS_l_TIMES']
        corresponding_event_numbers = [1, 2]

        for i, event_type in enumerate(relevant_event_types):
            event_number = corresponding_event_numbers[i] + 20 * (block_number - 1) # For each block, the event_ids are ordered within a range of 20 number 1-20, 21-40, etc.
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

    # Change to integer and sort events object
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    events_spikes = np.copy(events)
    events_spikes[:, 0] = events_spikes[:, 0] * params.sfreq_spikes / params.sfreq_raw
    events_spikes = events_spikes.astype(np.int64)

    return events, events_spikes, event_id
