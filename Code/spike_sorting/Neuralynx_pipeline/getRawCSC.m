clear; close all; clc;

%%  
% base_folder = fullfile('..', '..', '..', 'Data', 'UCLA', 'patient_479');

base_folder = '/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/patient_479';
output_path = fullfile(base_folder,'ChannelsCSC');

mkdir(output_path);
addpath(genpath('releaseDec2015'), genpath('functions'))
ncs_files = dir([base_folder '/Raw/*.ncs']);

%%
FieldSelection(1) = 1; %     1. Timestamps   
FieldSelection(2) = 1; %     2. Sc Numbers
FieldSelection(3) = 1; %     3. Cell Numbers
FieldSelection(4) = 1; %     4. Params
FieldSelection(5) = 1; %     5. Data Points

ExtractHeader = 0;
ExtractMode = 1;
ModeArray=[]; %all.

%%

idx=1;
for ncs_file_name=ncs_files'
    file_name = ncs_file_name.name;
    ncs_file = fullfile(base_folder,'Raw',file_name);
    fprintf('CSC of channnel %d...',idx);
    [Timestamps, ChannelNumbers, SampleFrequencies, NumberOfValidSamples, Samples, Header] = Nlx2MatCSC_v3(ncs_file,[1 1 1 1 1],1,1,1);
    data=reshape(Samples,1,size(Samples,1)*size(Samples,2));
    data=int16(data);
    samplingInterval = 1000/SampleFrequencies(1);
    save(fullfile(output_path,['CSC' num2str(idx) '.mat']),'data','samplingInterval', 'file_name');
    fprintf('saved as %s \n', fullfile(output_path,['CSC' num2str(idx) '.mat']));
    electrodes_info{idx} = ncs_file_name.name;
    idx = idx+1;
end
save(fullfile(base_folder, 'electrodes_info_names.mat'), 'electrodes_info')

%% !!! sampling rate !!!! - make sure it's correct
sr = 30000; 
% channels = 1:(idx-1); %idx=130 for UCLA patient 479
channels = [13, 47, 48, 49, 55, 57, 59];

%% get all csc and produce scs_spikes according to filter and threshold parameters  
Get_spikes_CSC_notch2k_ariel_mat (channels, fullfile(base_folder, 'ChannelsCSC'), sr) 

%% only for wave_clus use
ariel_do_clustering_csc(output_path, channels, sr) 


