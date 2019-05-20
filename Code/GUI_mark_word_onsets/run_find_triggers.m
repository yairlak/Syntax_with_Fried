clear all; close all; clc

%%
params.wav_file_number = 113; % '1.wav'
params.sr = 44100; % [Hz]
params.window_size = params.sr;
params.output_fname = 'English_stimuli_word_onsets.txt';
params.path2stimuli = fullfile('..', '..', 'Stimuli', 'Audio', 'normalized');

%%
find_triggers_in_wav_files(params)
    