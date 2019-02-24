import os
from tqdm import tqdm
import numpy as np
import mne

def load_data(path2data, path2electrode_info, patient_name, electrode_info_filename = 'TDT_elecs_all.mat', whole_block_flag=True):
    '''

    :param path2data:
    :param patient_name:
    :return:

    whole_block_flag == True:
    --------------------------
    (list of dicts) num_blocks. Each dict has the follwing keys:
    data        # ECoG data [chan x time]
    fs          # sampling rate of ECoG dat
    evnt        # (ndarray of dicts) num_events. Each dict has the following keys: {'name'}    {'ind'}    {'confidence'}
                                                                                   {'StartTime'} {'StopTime'} {'wname'}
                                                                                   {'expt'}    {'subject'}    {'block'}
                                                                                   {'exptind'}    {'trial'}   {'dpath'}

    whole_block_flag == False:
    --------------------------
    (ndarray of dicts) num_stimuli. Each stimulus-dict has the following keys
    name        # stimulus file name
    sound       # waveform of stimulus
    soundf      # sampling rate of stimulus
    dataf       # sampling rate of ECoG dat
    aud         # mel-frequency spectrogram of sound (80 frequency bands)
    duration    # duration of stimulus (sec)
    Trials      # trial numbers where the stimulus was played
    befaft      # time before stimulus onset and after stimulus offset (sec)
    resp        # ECoG data [chan x time x trials]; each stimulus was presented num_trials times.
    phnmat      # phoneme alignments [59 phonemes x time]
    diphnmat    # diphone alignments
    phnmatonset # phoneme onset times
    '''
    import glob
    import scipy.io as sio
    whole_block = 'wholeBlock' if whole_block_flag else 'epoched'
    filename_data = glob.glob(os.path.join(path2data, patient_name + '*v7*' + whole_block + '*.mat'))[0]
    # Electrode info
    electrode_info = {}
    electrode_info['labels'] = sio.loadmat(os.path.join(path2electrode_info, electrode_info_filename))['anatomy']
    electrode_info['coordinates'] = sio.loadmat(os.path.join(path2electrode_info, electrode_info_filename))['elecmatrix']
    if whole_block_flag:
        data = sio.loadmat(filename_data)['dat'][0]
    else:
        data = sio.loadmat(filename_data)['out'][0] # 'out' contains all information; the other var (syllfeats) is not relevant for the syntax project
    return data, electrode_info


def cat_all_trials(patient_data, whole_block_flag=True):
    '''

    :param patient_data: high-gamma normalized activity
    :param whole_block_flag: (boolean) type of input data - whether already epoched or whole-block
    :return: data_all_trials (ndarray) num_channel X num_time_samples
             event_times (list) num_stimuli.
             Each token of the list is also a list whose size is the number of repetitions the stimulus was presnted.
             The values are the event times in SAMPLES.
    '''

    if whole_block_flag:
        data_all_trials = []
        event_times = []
    else:
        num_channels = patient_data[0]['resp'].shape[0]
        sfreq_data = patient_data[0]['dataf'][0][0]
        ISI = 0.05 # sec
        event_times = []
        event_time_cnt = 0 + int(patient_data[0]['befaft'][0][0] * sfreq_data)
        data_all_trials = np.empty((num_channels, 0))
        time_before_stimulus = patient_data[0]['befaft'][0][0]

        patient_data = [patient_data[i]['resp'] for i in range(len(patient_data))]
        longest_trial = max([t.shape[1] for t in patient_data])

        data_all_trials = []
        for trial, curr_trial_data in enumerate(tqdm(patient_data)):
            curr_trial_length = curr_trial_data.shape[1]
            pad_length = 10 + longest_trial - curr_trial_length # Always add 5 sample (5ms)
            npad = ((0, 0), (0, pad_length), (0, 0))
            curr_trial_data = np.pad(curr_trial_data, pad_width=npad, mode='constant', constant_values=0)
            data_all_trials.append(curr_trial_data)
            patient_data[trial] = []

        import matplotlib.pyplot as plt
        event_times = []
        time_cnt = 0
        time_cnt = int(time_before_stimulus * sfreq_data)
        for tensor in data_all_trials:
            curr_stimulus_events = []
            num_repetitions = tensor.shape[2]
            for rep in range(num_repetitions):
                curr_stimulus_events.append(time_cnt)
                last_trial_length = tensor.shape[1]
                time_cnt += last_trial_length
            event_times.append(curr_stimulus_events)
        data_all_trials = [t.transpose(0, 2, 1) for t in data_all_trials]
        data_all_trials = [t.reshape((t.shape[0], -1), order='C') for t in data_all_trials]
        data_all_trials = np.concatenate(data_all_trials, axis=1)
    return data_all_trials, event_times



def get_word_strings(path2stimuli, stimulus_names):
    '''

    :param path2stimuli:
    :param stimulus_names:
    :return: list of dict (number of stimuli)
    '''

    stimuli_words = []
    print('Getting stimulus text information and parse it:')

    parse_folder = os.path.join(path2stimuli, '..', 'syntactic_labels')


    for stimulus_name in tqdm(stimulus_names):
        with open(os.path.join(path2stimuli, stimulus_name + '.wrd'), 'r') as f:
            word_info = f.readlines()
        words = [w.strip().split(' ')[-1] for w in word_info]
        word_onset = [w.strip().split(' ')[0] for w in word_info]  # Start time of word
        word_ofset = [w.strip().split(' ')[1] for w in word_info]  # End time of word
        sentence = ' '.join(words)

        with open(os.path.join(parse_folder, stimulus_name + '.syn'), 'r') as f:
            parse_info = f.readlines()
        pos = parse_info[1].strip().split(' ')
        parse = parse_info[2]

        # print(parse, pos)
        stimuli_words.append(
            {'sentence': sentence, 'parse': parse, 'POS': pos, 'words': words, 'word_onset': word_onset,
             'word_ofset': word_ofset})


    words = [s['words'] for s in stimuli_words]
    total_num_words = sum([len(w) for w in words])
    lexicon = list(set().union(*words))

    return stimuli_words, words, total_num_words, lexicon


def create_metadata(stimuli_words, event_times_start, event_times_stop, sfreq_data, sfreq_sound, whole_block_flag=True):
    import pandas as pd

    # Create a dict with the following keys:
    keys = ['event_time', 'sentence_number', 'sentence_string', 'word_position', 'word_string',
            'pos', 'num_words', 'last_word']
    metadata = dict([(k, []) for k in keys])


    if whole_block_flag:
        for stimulus, (stimulus_word, event_time_stimulus_sec) in enumerate(zip(stimuli_words, event_times_start)):
            for w, word in enumerate(stimulus_word['words']):  # Loop over all words in current sentence (trial)
                pos = stimulus_word['POS'][w] if len(stimulus_word['POS']) > 1 else ''
                metadata = add_event_to_metadata(metadata,
                                                 event_time=int((event_time_stimulus_sec + int(stimulus_word['word_onset'][w])/sfreq_sound)* sfreq_data),
                                                 sentence_number=stimulus + 1,
                                                 sentence_string=stimulus_word['sentence'],
                                                 word_position=w + 1,
                                                 word_string=word,
                                                 pos=pos,
                                                 num_words=len(stimulus_word['words']),
                                                 last_word= (w + 1 == len(stimulus_word['words']))
                                                 )
            # Add 'END' event: offset of the last word in each sentence
            if len(stimulus_word['words']) > 0:
                metadata = add_event_to_metadata(metadata,
                                                 event_time=int(event_times_stop[stimulus] * sfreq_data),
                                                 sentence_number=stimulus + 1,
                                                 sentence_string=stimulus_word['sentence'],
                                                 word_position=-1,
                                                 word_string='END',
                                                 pos='',
                                                 num_words=len(stimulus_word['words']),
                                                 last_word=False)

    else:
        for stimulus, (stimulus_word, event_times_stimulus) in enumerate(tqdm(zip(stimuli_words, event_times_start))):
            for event_time in event_times_stimulus:
                for w, word in enumerate(stimulus_word['words']): # Loop over all words in current sentence (trial)
                    pos = stimulus_word['POS'][w] if len(stimulus_word['POS']) > 1 else ''
                    metadata = add_event_to_metadata(metadata,
                                                     event_time=int(event_time + int(stimulus_word['word_onset'][w]) * sfreq_data / sfreq_sound),
                                                     sentence_number=stimulus + 1,
                                                     sentence_string=stimulus_word['sentence'],
                                                     word_position=w + 1,
                                                     word_string=word,
                                                     pos=pos,
                                                     num_words=len(stimulus_word['words']),
                                                     last_word=w + 1 == len(stimulus_word['words']))
                # Add 'END' event: offset of the last word in each sentence
                if len(stimulus_word['words']) > 0:
                    metadata = add_event_to_metadata(metadata,
                                                     event_time=int(event_time + int(stimulus_word['word_ofset'][-1]) * sfreq_data / sfreq_sound),
                                                     sentence_number=stimulus + 1,
                                                     sentence_string=stimulus_word['sentence'],
                                                     word_position=-1,
                                                     word_string='END',
                                                     pos='',
                                                     num_words=len(stimulus_word['words']),
                                                     last_word=False)



    metadata = pd.DataFrame(data=metadata)

    return metadata


def add_event_to_metadata(metadata, event_time, sentence_number, sentence_string, word_position, word_string, pos, num_words, last_word):
    metadata['event_time'].append(event_time)
    metadata['sentence_number'].append(sentence_number)
    metadata['sentence_string'].append(sentence_string)
    metadata['word_position'].append(word_position)
    metadata['word_string'].append(word_string)
    metadata['pos'].append(pos)
    metadata['num_words'].append(num_words)
    metadata['last_word'].append(last_word)
    return metadata

def convert_to_mne_python(data, events, event_id, electrode_info, metadata, sfreq_data, tmin, tmax):
    '''

    :param data:
    :param events:
    :param event_id:
    :param electrode_labels:
    :param metadata:
    :param sfreq_data:
    :param tmin:
    :param tmax:
    :return:
    '''
    channel_names = [s[0][0]+'-'+s[3][0] for s in electrode_info['labels']]
    regions = set([s[3][0] for s in electrode_info['labels']])
    print('Regions: ' + ' '.join(regions))
    montage = mne.channels.Montage(electrode_info['coordinates'], channel_names, 'misc', range(len(channel_names)))
    # fig_montage = montage.plot(kind='3d')
    num_channels = data.shape[0]
    ch_types = ['seeg' for s in range(num_channels)]
    info = mne.create_info(ch_names=channel_names, sfreq=sfreq_data, ch_types=ch_types)#, montage=montage)
    raw = mne.io.RawArray(data, info)

    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, metadata=metadata, baseline=None,
                        preload=False)
    return info, epochs



def create_events_array(metadata):
    '''

    :param metadata: (pandas dataframe) num_words X num_features; all words across all stimuli
    :param params: (object) general parameters
    :return:
    '''

    # First column of events object
    curr_times = np.expand_dims(metadata['event_time'].values, axis=1)

    # Second column
    second_column = np.zeros((len(curr_times), 1))

    # Third column
    event_numbers = range(len(curr_times))  # For each block, the event_ids are ordered within a range of 100 numbers block1: 101-201, block2: 201-300, etc.
    event_numbers = np.expand_dims(event_numbers, axis=1)

    # EVENT object: concatenate all three columns together (then change to int and sort)
    events = np.hstack((curr_times, second_column, event_numbers))
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    # EVENT_ID dictionary: mapping block names to event numbers
    event_id = dict([(str(event_type_name), event_number[0]) for event_type_name, event_number in zip(event_numbers, event_numbers)])


    return events, event_id


# !!!!!!!!!!!!!!!!!!!!!!! PARSING !!!!!!!!!!!!!!!!!!!!!
# See: https://stackoverflow.com/questions/13883277/stanford-parser-and-nltk/51981566#51981566
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# As of NLTK v3.3, users should avoid the Stanford NER or POS taggers from nltk.tag, and avoid Stanford tokenizer/segmenter from nltk.tokenize.
#
# Instead use the new nltk.parse.corenlp.CoreNLPParser API.
#
# Please see https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK
#
# (Avoiding link only answer, I've pasted the docs from NLTK github wiki below)
#
# First, update your NLTK
#
# pip3 install -U nltk # Make sure is >=3.3
# Then download the necessary CoreNLP packages:
#
# cd ~
# wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
# unzip stanford-corenlp-full-2018-02-27.zip
# cd stanford-corenlp-full-2018-02-27
#
# # Get the Chinese model
# wget http://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-02-27-models.jar
# wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-chinese.properties
#
# # Get the Arabic model
# wget http://nlp.stanford.edu/software/stanford-arabic-corenlp-2018-02-27-models.jar
# wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-arabic.properties
#
# # Get the French model
# wget http://nlp.stanford.edu/software/stanford-french-corenlp-2018-02-27-models.jar
# wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-french.properties
#
# # Get the German model
# wget http://nlp.stanford.edu/software/stanford-german-corenlp-2018-02-27-models.jar
# wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-german.properties
#
#
# # Get the Spanish model
# wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2018-02-27-models.jar
# wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-spanish.properties
# English
# Still in the stanford-corenlp-full-2018-02-27 directory, start the server:
#
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
# -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
# -status_port 9000 -port 9000 -timeout 15000 &
# Then in Python:
#
# >>> from nltk.parse import CoreNLPParser
#
# # Lexical Parser
# >>> parser = CoreNLPParser(url='http://localhost:9000')
#
# # Parse tokenized text.
# >>> list(parser.parse('What is the airspeed of an unladen swallow ?'.split()))
# [Tree('ROOT', [Tree('SBARQ', [Tree('WHNP', [Tree('WP', ['What'])]), Tree('SQ', [Tree('VBZ', ['is']), Tree('NP', [Tree('NP', [Tree('DT', ['the']), Tree('NN', ['airspeed'])]), Tree('PP', [Tree('IN', ['of']), Tree('NP', [Tree('DT', ['an']), Tree('JJ', ['unladen'])])]), Tree('S', [Tree('VP', [Tree('VB', ['swallow'])])])])]), Tree('.', ['?'])])])]
#
# # Parse raw string.
# >>> list(parser.raw_parse('What is the airspeed of an unladen swallow ?'))
# [Tree('ROOT', [Tree('SBARQ', [Tree('WHNP', [Tree('WP', ['What'])]), Tree('SQ', [Tree('VBZ', ['is']), Tree('NP', [Tree('NP', [Tree('DT', ['the']), Tree('NN', ['airspeed'])]), Tree('PP', [Tree('IN', ['of']), Tree('NP', [Tree('DT', ['an']), Tree('JJ', ['unladen'])])]), Tree('S', [Tree('VP', [Tree('VB', ['swallow'])])])])]), Tree('.', ['?'])])])]
#
# # Neural Dependency Parser
# >>> from nltk.parse.corenlp import CoreNLPDependencyParser
# >>> dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
# >>> parses = dep_parser.parse('What is the airspeed of an unladen swallow ?'.split())
# >>> [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses]
# [[(('What', 'WP'), 'cop', ('is', 'VBZ')), (('What', 'WP'), 'nsubj', ('airspeed', 'NN')), (('airspeed', 'NN'), 'det', ('the', 'DT')), (('airspeed', 'NN'), 'nmod', ('swallow', 'VB')), (('swallow', 'VB'), 'case', ('of', 'IN')), (('swallow', 'VB'), 'det', ('an', 'DT')), (('swallow', 'VB'), 'amod', ('unladen', 'JJ')), (('What', 'WP'), 'punct', ('?', '.'))]]
#
#
# # Tokenizer
# >>> parser = CoreNLPParser(url='http://localhost:9000')
# >>> list(parser.tokenize('What is the airspeed of an unladen swallow?'))
# ['What', 'is', 'the', 'airspeed', 'of', 'an', 'unladen', 'swallow', '?']
#
# # POS Tagger
# >>> pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
# >>> list(pos_tagger.tag('What is the airspeed of an unladen swallow ?'.split()))
# [('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), ('airspeed', 'NN'), ('of', 'IN'), ('an', 'DT'), ('unladen', 'JJ'), ('swallow', 'VB'), ('?', '.')]
#
# # NER Tagger
# >>> ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
# >>> list(ner_tagger.tag(('Rami Eid is studying at Stony Brook University in NY'.split())))
# [('Rami', 'PERSON'), ('Eid', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('Stony', 'ORGANIZATION'), ('Brook', 'ORGANIZATION'), ('University', 'ORGANIZATION'), ('in', 'O'), ('NY', 'STATE_OR_PROVINCE')]
