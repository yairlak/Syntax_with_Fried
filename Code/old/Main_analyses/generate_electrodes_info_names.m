clear all; close all; clc

%% Paths
path2raw = fullfile('..', '..', 'Data', 'UCLA', 'patient_493', 'Raw');
path2output = fullfile('..', '..', 'Data', 'UCLA', 'patient_493');
output_filename = 'electrodes_info_names.mat';

%%
ncs_files = dir(fullfile(path2raw, '*.ncs'));

electrodes_info = cell(1, length(ncs_files));
cnt = 1;
for f = ncs_files
    electrodes_info{cnt} = f.name;
    cnt = cnt + 1;
end

save(fullfile(path2output, output_filename), 'electrodes_info')