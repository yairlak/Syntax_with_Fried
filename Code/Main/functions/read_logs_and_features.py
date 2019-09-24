import numpy as np
import pickle, os
import math

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

                # sentences_start, sentences_end, sentences_length = get_sentences_start_end_length(self.SENTENCE_NUM_ORDER, settings)
                # setattr(self, 'sentences_start', sentences_start)
                # setattr(self, 'sentences_end', sentences_end)
                # setattr(self, 'sentences_length', sentences_length)

            else:
                setattr(self, event_type + '_TIMES', [i[0] for i in log_content if event_type == i[1]])
                event_types_added.append(event_type + '_TIMES')

        setattr(self, 'event_types', event_types_added)

        return self

def get_sentences_start_end_length(SENTENCE_NUM_ORDER, settings):
    # Load text containing all sentences
    with open(os.path.join(settings.path2stimuli, settings.stimuli_text_file), 'r') as f:
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


def load_features(settings):
    import pandas

    # Read features file ('xlsx')
    sheet = pandas.read_excel(os.path.join(settings.path2stimuli, settings.features_file))
    headers = sheet.columns
    fields = []
    for i, header in enumerate(headers):
        fields.append(sheet[header].values)
    features = {'headers': headers, 'fields': fields}

    return features


def extract_comparison(comparison_list, features, settings, preferences):
    trial_numbers = features['fields'][0][1::]
    stimuli = features['fields'][1][1::]
    features = features['fields'][2::]
    contrast_names = comparison_list['fields'][0]

    comparisons = []

    ### Comparisons
    for i, contrast_name in enumerate(contrast_names):
        if preferences.use_metadata_only:
            # blocks_list = comparison_list['fields'][5][settings.comparisons][i].split(';')
            # align_to_list = comparison_list['fields'][4][settings.comparisons][i].split(';')
            blocks = comparison_list['fields'][4][i]
            align_to = comparison_list['fields'][3][i]
            generalize_to_modality = comparison_list['fields'][7][i]
            generalize_to_contrast = comparison_list['fields'][8][i]
            # for b, blocks in enumerate(blocks_list):
            #     for align_to in align_to_list:
            curr_dict = {}
            curr_dict['contrast_name'] = contrast_name + '_' + str(blocks) + '_' + align_to
            curr_dict['contrast'] = comparison_list['fields'][1][i]
            curr_query = curr_dict['contrast'][1:-1].split(',')
            curr_query = [s.strip() for s in curr_query]
            curr_dict['query'] = curr_query
            cond_labels = comparison_list['fields'][2][i]
            curr_dict['cond_labels'] = cond_labels[1:-1].split(',')
            curr_dict['align_to'] = align_to
            curr_dict['blocks'] = blocks
            curr_dict['generalize_to_blocks'] = generalize_to_modality
            curr_dict['generalize_to_contrast'] = generalize_to_contrast
            sortings = comparison_list['fields'][5][i]
            if isinstance(sortings, str):
                curr_dict['sorting'] = sortings.split(',')
            else:
                curr_dict['sorting'] = []
            curr_dict['union_or_intersection'] = comparison_list['fields'][6][i]

            comparisons.append(curr_dict)

        else:
            print('Metadata is not used')

    return comparisons


def load_POS_tags(settings):
    with open(os.path.join(settings.path2stimuli, settings.word2pos_file), 'rb') as f:
        word2pos = pickle.load(f)

    return word2pos

def load_morphology(settings, morphology_filename='morphology.xlsx'):
    import pandas
    word2morpheme = {}
    sheet = pandas.read_excel(os.path.join(settings.path2stimuli, morphology_filename))
    words = sheet['word_string']
    morphemes = sheet['morpheme']
    morpheme_types = sheet['morpheme_type']

    for w, m, t in zip(words, morphemes, morpheme_types):
        if np.isnan(t):
            t=0
        if not isinstance(m, str):
            m=''
        word2morpheme[w.lower()] = (m, t)

    return word2morpheme

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

    word2morpheme = load_morphology(settings)

    trial_numbers = features['fields'][0][1::]
    stimuli = features['fields'][1][1::]
    features = features['fields'][2::]
    num_blocks = len(log_all_blocks)

    # Create a dict with the following keys:
    keys = ['chronological_order', 'event_time', 'block', 'sentence_number', 'word_position', 'word_string', 'pos',
            'num_letters', 'sentence_string', 'sentence_length', 'last_word', 'morpheme', 'morpheme_type']
    keys = keys + [col[0] for col in features if isinstance(col[0], str)]
    #keys = keys + [col[0] for col in features]
    metadata = dict([(k, []) for k in keys])

    cnt = 1
    for block, log in log_all_blocks.items():
        # Prefix according to visual/auditory
        if block in [1, 3, 5]: # Visual
            prefix = "DISPLAY_TEXT"
        elif block in [2, 4, 6]: # Auditory
            prefix = "AUDIO_PLAYBACK_ONSET"

        # Loop over all words in current log
        num_words = len(getattr(log, prefix + '_WORDS_ON_TIMES'))
        for i in range(num_words):
            metadata['chronological_order'].append(cnt); cnt += 1
            metadata['event_time'].append((int(getattr(log, 'WORDS_ON_TIMES')[i]) - settings.time0) / 1e6)
            sentence_number = getattr(log, 'SENTENCE_NUM')[i]
            metadata['block'].append(block)
            metadata['sentence_number'].append(sentence_number)
            metadata['word_position'].append(int(getattr(log, 'WORD_SERIAL_NUM')[i]))
            word_string = getattr(log, 'WORD_STRING')[i]
            if word_string[-1] == '?' or word_string[-1] == '.':
                word_string = word_string[0:-1]
            word_string = word_string.lower()
            metadata['word_string'].append(word_string)
            metadata['pos'].append(word2pos[word_string])
            metadata['morpheme'].append(word2morpheme[word_string][0])
            metadata['morpheme_type'].append(int(word2morpheme[word_string][1]))
            metadata['num_letters'].append(getattr(log, 'num_letters')[i])

            # Get features from Excel file
            IX = np.where(trial_numbers == int(sentence_number))[0]
            metadata['sentence_string'].append(stimuli[IX][0])
            metadata['sentence_length'].append(len(stimuli[IX][0].split(' ')))
            metadata['last_word'].append(metadata['sentence_length'][-1] == int(metadata['word_position'][-1]))
            [metadata[col[0]].append(col[IX+1][0]) for col in features if isinstance(col[0], str)]
            #[metadata[col[0]].append(col[IX+1][0]) for col in features]
            if metadata['last_word'][-1]: # Add end-of-sentence event after last words. Set its 'word_pos' = -1.
                metadata['chronological_order'].append(cnt); cnt += 1
                sentence_number = getattr(log, 'SENTENCE_NUM')[i]
                t = None
                if metadata['block'][-1] in [1, 3, 5]:
                    t = metadata['event_time'][-1] + params.word_ON_duration*1e-3
                elif metadata['block'][-1] in [2, 4, 6]:
                    t = (int(getattr(log, 'END_WAV_TIMES')[int(sentence_number)-1]) - settings.time0) / 1e6
                metadata['event_time'].append(t)
                metadata['block'].append(block)
                metadata['sentence_number'].append(sentence_number)
                metadata['word_position'].append(-1)
                metadata['word_string'].append('.')
                metadata['pos'].append('END')
                metadata['morpheme'].append('')
                metadata['morpheme_type'].append(-1)
                metadata['num_letters'].append(getattr(log, 'num_letters')[i])

                # Get features from Excel file
                IX = np.where(trial_numbers == int(sentence_number))[0]
                metadata['sentence_string'].append(stimuli[IX][0])
                metadata['sentence_length'].append(len(stimuli[IX][0].split(' ')))
                metadata['last_word'].append(False)
                [metadata[col[0]].append(col[IX + 1][0]) for col in features if isinstance(col[0], str)]

    metadata = pd.DataFrame(data=metadata)

    return metadata


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

