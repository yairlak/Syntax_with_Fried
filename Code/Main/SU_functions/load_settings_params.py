import os


class Settings:
    def __init__(self):
        # PATIENT:
        self.hospital = 'UCLA'
        self.patient = 'patient_479'
        self.load_line_filtered_resampled_epoch_object = False

        # PARADIGM
        self.blocks = [2]
        self.blocks_str = ''.join(str(x) for x in self.blocks)

        self.event_types_to_extract = ['FIRST_WORD_TIMES', 'LAST_WORD_TIMES', 'END_WAV_TIMES', 'KEY_PRESS_l_TIMES']
        self.event_numbers_to_assign_to_extracted_event_types = [1, 2, 3, 4]  # Should match the above (event_types_to_extract)
        # self.event_types_to_extract = ['FIRST_WORD_TIMES', 'LAST_WORD_TIMES', 'KEY_PRESS_l_TIMES']
        # self.event_numbers_to_assign_to_extracted_event_types = [1, 2, 3]  # Should match the above (event_types_to_extract)
        # self.events_to_plot = ['FIRST_WORD_TIMES_block_1', 'FIRST_WORD_TIMES_block_3']
        self.events_to_plot = ['END_WAV_TIMES_block_2']
        # self.events_to_plot = ['LAST_WORD_TIMES_block_1', 'LAST_WORD_TIMES_block_2', 'LAST_WORD_TIMES_block_3']
        # self.events_to_plot = ['KEY_PRESS_l_TIMES_block_1', 'KEY_PRESS_l_TIMES_block_2', 'KEY_PRESS_l_TIMES_block_3']

        self.SOA = 500 # [msec]

        # RECORDINGS/CHANNELS
        #self.channel = 28 # channel to process time-frequency analyses
        self.channels_with_spikes = [13, 47, 48, 49, 55, 57, 59] # which channels in the raw CSC files have clear spikes
        self.channels_with_spikes = [47, 56]
        self.channels_with_spikes = [6, 7, 13, 19, 20, 23, 26, 28, 33, 37, 38, 39, 40, 43, 47, 51, 55, 56, 57, 62, 65, 68, 70, 71, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94 ,95, 96, 98, 99, 100, 101, 103, 104]
        self.time0 = 0 # in [sec]
        self.timeend = 1.3636832e+09  # in [sec]
        self.timeend = 3.3636832e+09  # in [sec]
        self.time0 = 1489760586848367
        self.timeend = 1489763746079099
        # PATHS
        self.path2patient_folder = os.path.join('..', '..', 'Data', self.hospital, self.patient)
        self.path2log = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Logs')
        self.path2rawdata = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Raw')
        self.path2macro = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/' + self.patient + '/Macro/ChannelsCSC'
        self.path2epoch_data = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Epochs')
        self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
        self.path2output_spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2stimuli = os.path.join('..', '..', 'Paradigm')
        self.path2spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2figures = os.path.join('..', '..', 'Figures')

        # Files info
        self.log_name_beginning = 'new_events_log_in_cheetah_clock_block'
        self.log_name_beginning = 'new_mouse_recording_in_cheetah_clock_part'
        self.stimuli_file = 'features En_02 sentences.xlsx'
        self.sentences_start_end_filename = 'sentences_start_end_dict.pkl'
        self.stimuli_text_file = 'sentences_Eng_rand_En02.txt'


class Preferences:
    def __init__(self):
        self.analyze_micro_single = False
        self.analyze_micro_raw = False
        self.analyze_macro = True
        self.sort_according_to_sentence_length = False
        self.step = 20 # yticklabels step when showing the length of each trial


class Params:
    def __init__(self):
        self.sfreq_raw = 40000 # Data sampling frequency [Hz]
        self.sfreq_spikes = 100 # dummy frequency for rasters via MNE [Hz]
        self.line_frequency = [60, 120, 180, 240]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec], should be negative
        self.tmax = 3 # End time after event [sec]
        self.ylim_PSTH = 20 # maximal frequency to present in PSTH [Hz]
        self.downsampling_sfreq = 512
        self.iter_freqs = [('High-Gamma', 70, 150)]
        self.freq_step = 2  # [Hz] Step in spectrogram
        # self.time_step = self.tmax * self.sfreq_raw # Epoch into subsequent segments\
        # self.slice_size = 500 * self.sfreq

