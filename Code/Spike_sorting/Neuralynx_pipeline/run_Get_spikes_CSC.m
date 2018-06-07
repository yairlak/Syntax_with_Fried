clear; close all; clc;

%%
patient = 'patient_482';

base_folder = ['/home/yl254115/Projects/single_unit_syntax/Data/UCLA/', patient];
% base_folder = ['/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/', patient];
output_path = fullfile(base_folder,'ChannelsCSC');

% mkdir(output_path);
addpath(genpath('releaseDec2015'), genpath('NPMK-4.5.3.0'), genpath('functions'))
rmpath(genpath(fullfile('..', 'wave_clus-testing')))

%% !!! sampling rate !!!! - make sure it's correct
sr = 40000; 
channels = 63:88;
%channels = [26, 28, 51];
% channels = [17:18];
not_neuroport = 1;

%% get all csc and produce scs_spikes according to filter and threshold parameters  
Get_spikes_CSC_notch2k_ariel_mat (channels, fullfile(base_folder, 'ChannelsCSC'), not_neuroport, sr) 