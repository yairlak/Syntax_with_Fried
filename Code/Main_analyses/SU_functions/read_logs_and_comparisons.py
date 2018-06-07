import numpy as np
import pickle, os

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
        event_types_in_paradigm_log = [i[1] for i in log_content]
        event_types_in_paradigm_log = list(set().union(event_types_in_paradigm_log, event_types_in_paradigm_log))

        # For each event type, extract onset times and stimulus information
        event_types_added = []
        for event_type in event_types_in_paradigm_log:
            if event_type == 'DISPLAY_TEXT':
                setattr(self, event_type + '_WORDS_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_WORDS_ON_TIMES')
                setattr(self, event_type + '_WORD_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_WORD_NUM')
                setattr(self, event_type + '_SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_SENTENCE_NUM')
                setattr(self, event_type + '_WORD_SERIAL_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_WORD_SERIAL_NUM')
                setattr(self, event_type + '_WORD_STRING', [i[5] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append(event_type + '_WORD_STRING')
                setattr(self, 'FIRST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF' if i[4] == '1'])
                event_types_added.append('FIRST_WORD_TIMES')
                setattr(self, 'SENTENCE_NUM', [i[3] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append('SENTENCE_NUM')
                setattr(self, 'WORD_SERIAL_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append('WORD_SERIAL_NUM')
                self.SENTENCE_NUM_ORDER = []; last_sent=[]
                for i in self.SENTENCE_NUM:
                    if i!=last_sent:
                        self.SENTENCE_NUM_ORDER.append(int(i))
                        last_sent = i
                event_types_added.append('SENTENCE_NUM_ORDER')
                setattr(self, event_type + '_OFF_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'OFF']) # WORD-IMAGE IS 'OFF'
                event_types_added.append(event_type + '_OFF_TIMES')

                setattr(self, 'WORD_STRING', [i[5] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append('WORD_STRING')
                setattr(self, 'WORDS_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF'])
                event_types_added.append('WORDS_ON_TIMES')

                sentences_start, sentences_end, sentences_length = get_sentences_start_end_length(self.SENTENCE_NUM_ORDER, settings)
                setattr(self, 'FIRST_WORD_TIMES1', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF' if int(i[2]) in sentences_start.values()])
                event_types_added.append('FIRST_WORD_TIMES1') # SANITY CHECK: FIRST_WORD_TIMES=FIRST_WORD_TIMES1
                setattr(self, 'LAST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != 'OFF' if int(i[2]) in sentences_end.values()])
                event_types_added.append('LAST_WORD_TIMES')

                word_strings_parsed = [s[0:-1] if s[-1] in ['.', '?'] else s for s in self.WORD_STRING]
                num_letters = [len(s) for s in word_strings_parsed]
                setattr(self, 'num_letters', num_letters)
                event_types_added.append('num_letters')

            elif event_type == 'AUDIO_PLAYBACK_ONSET':
                setattr(self, event_type + '_WORDS_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_WORDS_ON_TIMES')
                setattr(self, event_type + '_WORD_NUM', [i[2] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_WORD_NUM')
                setattr(self, event_type + '_WAV_FILE', [i[3] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append('SENTENCE_NUM')
                setattr(self, event_type + '_WORD_SERIAL_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_WORD_SERIAL_NUM')
                setattr(self, event_type + '_WORD_STRING', [i[5] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_WORD_STRING')

                setattr(self, 'FIRST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_' if i[4] == '1'])
                event_types_added.append('FIRST_WORD_TIMES')
                setattr(self, 'SENTENCE_NUM',
                [i[3].split('.')[0] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append(event_type + '_SENTENCE_NUM')
                setattr(self, 'WORD_SERIAL_NUM', [i[4] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append('WORD_SERIAL_NUM')

                self.SENTENCE_NUM_ORDER = []; last_sent = []
                for i in self.SENTENCE_NUM:
                    if i != last_sent:
                        self.SENTENCE_NUM_ORDER.append(int(i))
                        last_sent = i
                event_types_added.append('SENTENCE_NUM_ORDER')

                setattr(self, 'END_WAV_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == '_'])
                event_types_added.append('END_WAV_TIMES')

                setattr(self, 'WORD_STRING', [i[5] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append('WORD_STRING')

                sentences_start, sentences_end, sentences_length = get_sentences_start_end_length(self.SENTENCE_NUM_ORDER, settings)
                setattr(self, 'FIRST_WORD_TIMES1', [i[0] for i in log_content if event_type == i[1] and i[2] != '_' if int(i[2]) in sentences_start.values()])
                event_types_added.append('FIRST_WORD_TIMES1')  # SANITY CHECK: FIRST_WORD_TIMES=FIRST_WORD_TIMES1
                setattr(self, 'LAST_WORD_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_' if int(i[2]) in sentences_end.values()])
                event_types_added.append('LAST_WORD_TIMES')
                setattr(self, 'WORDS_ON_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] != '_'])
                event_types_added.append('WORDS_ON_TIMES')

                setattr(self, 'sentences_start', sentences_start)
                setattr(self, 'sentences_end', sentences_end)
                setattr(self, 'sentences_length', sentences_length)

                word_strings_parsed = [s[0:-1] if s[-1] in ['.', '?'] else s for s in self.AUDIO_PLAYBACK_ONSET_WORD_STRING]
                
                num_letters = [len(s) for s in word_strings_parsed]
                setattr(self, 'num_letters', num_letters)
                event_types_added.append('num_letters')

            elif event_type == 'KEY_PRESS':
                setattr(self, event_type + '_SPACE_TIMES', [i[0] for i in log_content if event_type == i[1] and i[2] == 'space'])
                event_types_added.append(event_type + '_SPACE_TIMES')
                list_of_key_press_times = []; previous_key_press_time = 0.
                for cnt, i in enumerate(log_content):
                    if event_type == i[1] and i[2] == 'l' and np.abs(previous_key_press_time-float(i[0]))>1e6: # only if time between two key presses is greater than 1sec
                        list_of_key_press_times.append(i[0])
                        previous_key_press_time = float(i[0])
                setattr(self, event_type + '_l_TIMES', list_of_key_press_times)
                event_types_added.append(event_type + '_l_TIMES')

                sentences_start, sentences_end, sentences_length = get_sentences_start_end_length(self.SENTENCE_NUM_ORDER, settings)
                setattr(self, 'sentences_start', sentences_start)
                setattr(self, 'sentences_end', sentences_end)
                setattr(self, 'sentences_length', sentences_length)

            else:
                setattr(self, event_type + '_TIMES', [i[0] for i in log_content if event_type == i[1]])
                event_types_added.append(event_type + '_TIMES')

        setattr(self, 'event_types', event_types_added)

        return self

def get_sentences_start_end_length(SENTENCE_NUM_ORDER, settings):
    # Load text containing all sentences
    with open(os.path.join(settings.path2patient_folder, settings.stimuli_text_file), 'r') as f:
        stimuli_sentences = f.readlines()
    sentences_length = [len(s.split(' ')) for s in stimuli_sentences]
    IX = [i-1 for i in SENTENCE_NUM_ORDER] # shift to count from zero
    sentences_length = np.asarray(sentences_length)[IX] #reorder array according to the (random) order of current block
    sentences_end = np.cumsum(sentences_length)
    sentences_start = [e-l+1 for (e, l) in zip(sentences_end, sentences_length)]

    sentences_length = dict(zip(range(1, len(sentences_length) + 1, 1), sentences_length))
    sentences_end = dict(zip(range(1, len(sentences_end) + 1, 1), sentences_end))
    sentences_start = dict(zip(range(1, len(sentences_start) + 1, 1), sentences_start))

    return sentences_start, sentences_end, sentences_length


def load_comparisons_and_features(settings):
    import pandas

    # Read comparison file ('xlsx')
    sheet = pandas.read_excel(os.path.join(settings.path2stimuli, settings.comparisons_file))
    headers = sheet.columns
    fields = []
    for i, header in enumerate(headers):
        fields.append(sheet[header].values)
        comparison_list = {'headers':headers, 'fields':fields}

    del sheet, headers

    # Read features file ('xlsx')
    sheet = pandas.read_excel(os.path.join(settings.path2stimuli, settings.features_file))
    headers = sheet.columns
    fields = []
    for i, header in enumerate(headers):
        fields.append(sheet[header].values)
    features = {'headers': headers, 'fields': fields}

    return comparison_list, features


def extract_comparison(contrast_names, contrasts, align_to, blocks, union_or_intersection, features, preferences):
    trial_numbers = features['fields'][0][1::]
    stimuli = features['fields'][1][1::]
    features = features['fields'][2::]

    comparisons = []

    ### Comparisons
    for i, contrast in enumerate(contrasts):

        if preferences.use_metadata_only:
            list_of_queries = contrast[1:-1].split(',')
            list_of_queries = [s.strip() for s in list_of_queries]
            comparisons.append(list_of_queries)
        else:
            contrast = str(contrast[2:-2]).split('],[')
            trial_numbers_and_strings = []
            for j, columns_condition in enumerate(contrast):
                columns_condition = columns_condition.split(',')
                columns_condition = [int(s) for s in columns_condition]
                binary_values_in_columns = [binary_values[1::] for col, binary_values in enumerate(features) if col+3 in columns_condition] # +3: Assumes features in XLS starts at column C
                if bool(union_or_intersection[i][j]):
                    IX_trials_curr_cond = np.prod(np.asarray(binary_values_in_columns), axis=0) == 1 # AND
                else:
                    IX_trials_curr_cond = np.sum(np.asarray(binary_values_in_columns), axis=0) > 0 # OR
                curr_trial_numbers = trial_numbers[IX_trials_curr_cond]
                curr_stimuli = stimuli[IX_trials_curr_cond]
                IX_sort = np.argsort(curr_trial_numbers)
                trial_numbers_and_strings.append({'trial_numbers':curr_trial_numbers[IX_sort], 'stimuli':curr_stimuli[IX_sort]})
            comparisons.append([trial_numbers_and_strings, align_to[i], contrast_names[i]])

    return comparisons


def load_POS_tags(settings):
    with open(os.path.join(settings.path2stimuli, settings.word2pos_file), 'rb') as f:
        word2pos = pickle.load(f)

    return word2pos


def prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences):
    '''

    :param log_all_blocks: list len = #blocks
    :param features: numpy
    :param settings:
    :param params:
    :param preferences:
    :return: metadata: list
    '''
    import pandas as pd

    trial_numbers = features['fields'][0][1::]
    stimuli = features['fields'][1][1::]
    features = features['fields'][2::]
    num_blocks = len(log_all_blocks)

    # Create a dict with the following keys:
    keys = ['chronological_order', 'event_time', 'block', 'sentence_number', 'word_position', 'word_string', 'pos',
            'num_letters', 'sentence_string', 'sentence_length', 'last_word']
    keys = keys + [col[0] for col in features if isinstance(col[0], unicode)]
    metadata = dict([(k, []) for k in keys])

    cnt = 1
    for block, log in enumerate(log_all_blocks):
        # Prefix according to visual/auditory
        if block + 1 in [1, 3, 5]: # Visual
            prefix = "DISPLAY_TEXT"
        elif block + 1 in [2, 4, 6]: # Auditory
            prefix = "AUDIO_PLAYBACK_ONSET"

        # Loop over all words in current log
        num_words = len(getattr(log, prefix + '_WORDS_ON_TIMES'))
        for i in range(num_words):
            metadata['chronological_order'].append(cnt); cnt += 1
            metadata['event_time'].append((int(getattr(log, 'WORDS_ON_TIMES')[i]) - settings.time0) / 1e6)
            sentence_number = getattr(log, 'SENTENCE_NUM')[i]
            metadata['block'].append(block + 1)
            metadata['sentence_number'].append(sentence_number)
            metadata['word_position'].append(int(getattr(log, 'WORD_SERIAL_NUM')[i]))
            word_string = getattr(log, 'WORD_STRING')[i]
            if word_string[-1] == '?' or word_string[-1] == '.':
                word_string = word_string[0:-1]
            word_string = word_string.lower()
            metadata['word_string'].append(word_string)
            metadata['pos'].append(word2pos[word_string])
            metadata['num_letters'].append(getattr(log, 'num_letters')[i])

            # Get features from Excel file
            IX = np.where(trial_numbers == int(sentence_number))[0]
            metadata['sentence_string'].append(stimuli[IX][0])
            metadata['sentence_length'].append(len(stimuli[IX][0].split(' ')))
            metadata['last_word'].append(metadata['sentence_length'][-1] == int(metadata['word_position'][-1]))
            [metadata[col[0]].append(col[IX+1][0]) for col in features if isinstance(col[0], unicode)]
            if metadata['last_word'][-1]: # Add end-of-sentence event after last words. Set its 'word_pos' = -1.
                metadata['chronological_order'].append(cnt); cnt += 1
                sentence_number = getattr(log, 'SENTENCE_NUM')[i]
                t = None
                if metadata['block'][-1] in [1, 3, 5]:
                    t = metadata['event_time'][-1] + params.word_ON_duration*1e-3
                elif metadata['block'][-1] in [2, 4, 6]:
                    t = (int(getattr(log, 'END_WAV_TIMES')[int(sentence_number)-1]) - settings.time0) / 1e6
                metadata['event_time'].append(t)
                metadata['block'].append(block + 1)
                metadata['sentence_number'].append(sentence_number)
                metadata['word_position'].append(-1)
                metadata['word_string'].append('.')
                metadata['pos'].append('END')
                metadata['num_letters'].append(getattr(log, 'num_letters')[i])

                # Get features from Excel file
                IX = np.where(trial_numbers == int(sentence_number))[0]
                metadata['sentence_string'].append(stimuli[IX][0])
                metadata['sentence_length'].append(len(stimuli[IX][0].split(' ')))
                metadata['last_word'].append(False)
                [metadata[col[0]].append(col[IX + 1][0]) for col in features if isinstance(col[0], unicode)]

    metadata = pd.DataFrame(data=metadata)

    return metadata