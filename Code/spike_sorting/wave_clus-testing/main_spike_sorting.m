clear all; close all; clc

%%
addpath(fullfile('..', 'wave_clus-testing'))
base_folder = fullfile('..', '..', '..', 'Data', 'tmp');
output_path = fullfile(base_folder,'ChannelsCSC');
mkdir(output_path);
addpath(genpath('releaseDec2015'), genpath('functions'))
ncs_files = dir([base_folder '/*.ncs']);

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
    ncs_file = fullfile(base_folder, file_name);
    [Timestamps, ChannelNumbers, SampleFrequencies, NumberOfValidSamples, Samples, Header] = Nlx2MatCSC_v3(ncs_file,[1 1 1 1 1],1,1,1);
    data=reshape(Samples,1,size(Samples,1)*size(Samples,2));
    data=int16(data);
    samplingInterval = 1000/SampleFrequencies(1);
    save(fullfile(output_path,['CSC' num2str(idx) '.mat']),'data','samplingInterval', 'file_name');
    fprintf('CSC of channnel %d saved\n',idx);
    electrodes_info{idx} = ncs_file_name.name;
    idx = idx+1;
end