import os


class Preferences:
    def __init__(self):
        self.analyze_micro_single = False
        self.analyze_micro_raw = True
        self.run_contrasts = True
        self.run_POS = False
        self.use_metadata_only = True
        self.step = 30 # yticklabels step when showing the length of each trial
        import sys
        if (self.run_contrasts + self.run_POS) > 1:
            sys.exit('In Preferences - either run_contrast or run_POS, not both')

class Settings():
    def __init__(self):
        # PATIENT:
        self.hospital = 'UCLA'
        self.patient = 'patient_479'
        self.comparisons = [16] # List of int:  defines which comparisons to execute from xls. If set to 'None' then all comparisons in the file are executed.
        self.load_line_filtered_resampled_epoch_object = False
        self.overwrite_existing_output_files = True


        # RECORDINGS/CHANNELS
        # Which channels in the raw CSC files have clear spikes
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
        #self.path2macro = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/' + self.patient + '/Macro/ChannelsCSC'
        #self.path2macro =  os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Macro', 'ChannelsCSC')
        self.path2epoch_data = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Epochs')
        # self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
        self.path2rawdata_mat = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/' + self.patient + '/ChannelsCSC'
        self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
        self.path2output_spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2stimuli = os.path.join('..', '..', 'Paradigm')
        self.path2spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2figures = os.path.join('..', '..', 'Figures')
        self.path2output = os.path.join('..', '..', 'Output')

        # Files info
        self.log_name_beginning = 'new_events_log_in_cheetah_clock_block'
        self.log_name_beginning = 'new_mouse_recording_in_cheetah_clock_part'
        self.stimuli_file = 'features En_02 sentences.xlsx'
        self.sentences_start_end_filename = 'sentences_start_end_dict.pkl'
        self.stimuli_text_file = 'sentences_Eng_rand_En02.txt'
        self.comparisons_file = 'comparisons_' + self.patient + '.xlsx'
        self.features_file = 'features_' + self.patient + '.xlsx'
        self.word2pos_file = 'word2POS.pkl'


class Params:
    def __init__(self):
        self.sfreq_raw = 40000 # Data sampling frequency [Hz]
        self.sfreq_spikes = 100 # dummy frequency for rasters via MNE [Hz]
        self.line_frequency = [50, 100, 150, 200]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec], should be negative
        self.tmax = 3 # End time after event [sec]
        self.ylim_PSTH = 20 # maximal frequency to present in PSTH [Hz]
        self.downsampling_sfreq = 512

        ###### Frequency bands ##########
        self.iter_freqs = [('High-Gamma', 70, 150)]
        # self.iter_freqs = []
        step = 5
        # for freq in range(4, 146, 1):
        #     band = str(freq) + '_to_' + str(freq + step) + 'Hz'
        #     self.iter_freqs.append((band, freq, freq + step))
        self.freq_step = 2  # [Hz] Step in spectrogram
        # self.time_step = self.tmax * self.sfreq_raw # Epoch into subsequent segments\
        # self.slice_size = 500 * self.sfreq
        ##################################

        ####### Time-frequency ###########
        self.temporal_resolution = 0.05  # Wavelet's time resolution [sec]
        self.smooth_time_freq = 50 * 1e-3 * self.downsampling_sfreq  # Size of window for Gaussian smoothing the time-freq results. Zero means no smoothing.
        self.smooth_time_freq = 0
        ##################################

        ####### Paradigm  #################
        self.SOA = 500  # [msec]
        self.word_ON_duration = 200 # [msec]
        self.word_OFF_duration = 300  # [msec]
        self.baseline_period = 500 # [msec]
        self.window_st = 50 # [msec] beginning of averaging window used for the vertical plot, relative time 0
        self.window_ed = 250  # [msec] end of averaging window used for the vertical plot, relative to time 0

        if self.baseline_period > abs(self.tmin)*1000:
            import sys
            sys.exit('Basline period must be longer than tmin. Otherwise, baseline cannot be computed.')

        ###################################
