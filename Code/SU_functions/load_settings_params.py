import os


class Settings:
    def __init__(self):
        # PATIENT:
        self.hospital = 'UCLA'
        self.patient = 'patient_479'
        self.load_line_filtered_resampled_epoch_object = True

        # PARADIGM
        self.blocks = [1, 3, 5]
        self.blocks_str = ''.join(str(x) for x in self.blocks)
        self.events_to_plot = ['FIRST_WORD_TIMES_block_1', 'FIRST_WORD_TIMES_block_3', 'FIRST_WORD_TIMES_block_5']

        # RECORDINGS/CHANNELS
        self.channel = 52 # channel to process time-frequency analyses
        self.channels_with_spikes = [13, 47, 48, 49, 55, 57, 59] # which channels in the raw CSC files have clear spikes

        # PATHS
        self.path2patient_folder = os.path.join('..', '..', 'Data', self.hospital, self.patient)
        self.path2log = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Logs')
        self.path2rawdata = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Raw')
        self.path2epoch_data = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Epochs')
        self.path2rawdata_mat = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'ChannelsCSC')
        self.path2output_spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2stimuli = os.path.join('..', '..', 'Paradigm')
        self.path2spike_clusters = os.path.join('..', '..', 'Data', self.hospital, self.patient, 'Spike_clusters')
        self.path2figures = os.path.join('..', '..', 'Figures')

        # Files info
        self.log_name_beginning = 'new_mouse_recording_in_cheetah_clock_part'
        self.stimuli_file = 'features En_02 sentences.xlsx'



class Params:
    def __init__(self):
        self.sfreq_raw = 30000 # Data sampling frequency [Hz]
        self.sfreq_spikes = 100 # dummy frequency for rasters via MNE [Hz]
        self.line_frequency = [60, 120, 180, 240]  # Line frequency [Hz]
        self.tmin = -3  # Start time before event [sec]
        self.tmax = 3 # End time after event [sec]
        self.downsampling_sfreq = 300
        self.iter_freqs = [('High-Gamma', 70, 150)]
        self.freq_step = 2  # [Hz] Step in spectrogram
        # self.time_step = self.tmax * self.sfreq_raw # Epoch into subsequent segments\
        # self.slice_size = 500 * self.sfreq
