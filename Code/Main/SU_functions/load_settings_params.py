import os


class Settings:
    def __init__(self):
        # PATIENT:
        self.hospital = 'UCLA'
        self.patient = 'patient_479'
        self.load_line_filtered_resampled_epoch_object = False

        # BLOCKS in paradigm to process
        self.blocks = [1, 3, 5]
	self.blocks = [2, 4, 6]
        self.blocks_str = ''.join(str(x) for x in self.blocks)

        if set(self.blocks) & set([2,4,6]): # Which events to add to MNE events array
            self.event_types_to_extract = ['FIRST_WORD_TIMES', 'LAST_WORD_TIMES', 'END_WAV_TIMES', 'KEY_PRESS_l_TIMES']
            self.event_types_to_extract = ['WORDS_ON_TIMES']
            self.event_numbers_to_assign_to_extracted_event_types = [1, 2, 3, 4, 5]  # Should match the above (event_types_to_extract)
            self.event_numbers_to_assign_to_extracted_event_types = [1]
        else:
            self.event_types_to_extract = ['FIRST_WORD_TIMES', 'LAST_WORD_TIMES', 'KEY_PRESS_l_TIMES', 'WORDS_ON_TIMES']
            self.event_types_to_extract = ['WORDS_ON_TIMES']
            self.event_numbers_to_assign_to_extracted_event_types = [1, 2, 3, 4]  # Should match the above (event_types_to_extract)
            self.event_numbers_to_assign_to_extracted_event_types = [1]  # Should match the above (event_types_to_extract)

        self.events_to_plot = ['FIRST_WORD_TIMES_block_1', 'FIRST_WORD_TIMES_block_2', 'FIRST_WORD_TIMES_block_3']
        # self.events_to_plot = ['END_WAV_TIMES_block_2', 'END_WAV_TIMES_block_4', 'END_WAV_TIMES_block_6']
        # self.events_to_plot = ['LAST_WORD_TIMES_block_1', 'LAST_WORD_TIMES_block_2', 'LAST_WORD_TIMES_block_3']
        # self.events_to_plot = ['KEY_PRESS_l_TIMES_block_1', 'KEY_PRESS_l_TIMES_block_2', 'KEY_PRESS_l_TIMES_block_3']

        # Event colors
        keys = [i+j for i in range(100, 700, 100) for j in range(1,5,1)]
        values = [c for i in range(1,7,1) for c in ['red', 'green', 'blue', 'k']]
        self.event_colors = dict(zip(keys,values))

        # RECORDINGS/CHANNELS
        # Which channels in the raw CSC files have clear spikes
        #self.channel = 28 # channel to process time-frequency analyses
        self.channels_with_spikes = [13, 47, 48, 49, 55, 57, 59]
        self.channels_with_spikes = [47, 56]
        if self.patient == 'patient_480':
            self.channels_with_spikes = [6, 7, 13, 19, 20, 23, 26, 28, 33, 37, 38, 39, 40, 43, 47, 51, 55, 56, 57, 62, 65, 68, 70, 71, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94 ,95, 96, 98, 99, 100, 101, 103, 104]

        # Time of the beginning and end of the experiment (BlackRock time0 = 0; In Neurlaynx it is measured compared to 01/01/1970)
        if self.patient == 'patient_479':
            self.time0 = 1489760586848367
            self.timeend = 1489763746079099
        if self.patient == 'patient_480':
            self.time0 = 0  # in [sec]
            self.timeend = 3.313463366666667e+09 # patient 480

            # self.timeend = 1.3636832e+09  # in [sec]
            # self.timeend = 3.3636832e+09  # in [sec]
            # settings.timeend = 3.159231975000000e+09

        # PATHS
        self.path2patient_folder = os.path.join('..', '..', 'Data', self.hospital, self.patient)
        self.path2log = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Logs')
        self.path2rawdata = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Raw')
        self.path2macro = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/' + self.patient + '/Macro/ChannelsCSC'
        #self.path2macro =  os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Macro', 'ChannelsCSC')
        self.path2epoch_data = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Epochs')
        # self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
        self.path2rawdata_mat = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/' + self.patient + '/ChannelsCSC'
        #self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
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
        self.analyze_micro_raw = True
        self.analyze_macro = True
        self.sort_according_to_sentence_length = False
        self.sort_according_to_num_letters = True
        self.step = 20 # yticklabels step when showing the length of each trial
        if (self.sort_according_to_sentence_length + self.sort_according_to_num_letters) > 1:
            import sys
            sys.exit('Too many sorting flags in Preferences')


class Params:
    def __init__(self):
        self.sfreq_raw = 40000 # Data sampling frequency [Hz]
        self.sfreq_spikes = 100 # dummy frequency for rasters via MNE [Hz]
        self.line_frequency = [50, 100, 150, 200]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec], should be negative
        self.tmax = 3 # End time after event [sec]
        self.ylim_PSTH = 20 # maximal frequency to present in PSTH [Hz]
        self.downsampling_sfreq = 512
        self.iter_freqs = [('High-Gamma', 70, 150)]
        self.freq_step = 2  # [Hz] Step in spectrogram
        # self.time_step = self.tmax * self.sfreq_raw # Epoch into subsequent segments\
        # self.slice_size = 500 * self.sfreq

        # Paradigm

        self.SOA = 500  # [msec]
        self.word_ON_duration = 200 # [msec]
        self.word_OFF_duration = 300  # [msec]
        self.baseline_period = 500 # [msec]
        self.window_st = 200 # [msec] beginning of averaging window used for the vertical plot, relative time 0
        self.window_ed = 500  # [msec] end of averaging window used for the vertical plot, relative to time 0

        if self.baseline_period > abs(self.tmin)*1000:
            import sys
            sys.exit('Basline period must be longer than tmin. Otherwise, baseline cannot be computed.')
