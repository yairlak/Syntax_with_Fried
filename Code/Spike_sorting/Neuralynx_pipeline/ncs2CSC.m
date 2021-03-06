clear; close all; clc;
addpath(genpath('releaseDec2015'), genpath('NPMK-4.5.3.0'), genpath('functions'))

%%
patient = 'patient_510';
elec_type = 'micro'; % micro / macro
recording_system = 'BlackRock'; % Neuralynx / BlackRock

%% pathsls 
base_folder = ['/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/', patient];
output_path = fullfile(base_folder, 'Raw', elec_type, 'CSC_mat');
mkdir(output_path);

%%
%
switch recording_system
        case 'Neuralynx'
            % Extract time0 and timeend from NEV file
            nev_filename = fullfile(base_folder, 'nev_files', 'Events.nev');
            
            % Extract raw data and save into MAT files
            ncs_files = dir(fullfile(base_folder, 'Raw', elec_type, 'ncs', '*.ncs'));
            idx=1;
            for ncs_file_name=ncs_files'
                fprintf('CSC of channnel %d...',idx);
                %
                file_name = ncs_file_name.name;
                fprintf('%s\n', ncs_file_name.name)
                ncs_file = fullfile(ncs_file_name.folder, ncs_file_name.name);
                %
                [Timestamps, ChannelNumbers, SampleFrequencies, NumberOfValidSamples, Samples, Header] = Nlx2MatCSC_v3(ncs_file,[1 1 1 1 1],1,1,1);
                data=reshape(Samples,1,size(Samples,1)*size(Samples,2));
                data=int16(data);
                samplingInterval = 1000/SampleFrequencies(1);
                fprintf('Sampling freq:')
                fprintf('%i\n', SampleFrequencies(1))
                save(fullfile(output_path,['CSC' num2str(idx) '.mat']),'data','samplingInterval', 'file_name');
                fprintf('saved as %s \n', fullfile(output_path,['CSC' num2str(idx) '.mat']));
                electrodes_info{idx} = ncs_file_name.name;
                idx = idx+1;
            end
        
        case 'BlackRock'
            ns5_files = dir(fullfile(base_folder, 'Raw', elec_type, 'ns', '*.ns5'));
            assert(length(ns5_files)==1, 'A SINGLE ns5 file in folder is expected')
            for ns_file_name=ns5_files'
                file_name = ns_file_name.name;
                NS5=openNSx(fullfile(ns_file_name.folder,  ns_file_name.name),'precision','double')
                samplingFreq = NS5.MetaTags.SamplingFreq
                samplingInterval = 1/samplingFreq;
                timeend_sec = NS5.MetaTags.DataDurationSec
                idx=1;
                for elec = 104:size(NS5.Data, 1)
                   elec_name = NS5.ElectrodesInfo(elec).Label
                   data = NS5.Data(elec, :);
                   fprintf('Sampling freq:')
                   fprintf('%i\n', samplingFreq)
                   fprintf('%s\n', elec_name)
                   save(fullfile(output_path,['CSC' num2str(idx) '.mat']),'data','samplingInterval', 'elec_name');
                   electrodes_info{idx} = elec_name;
                   idx = idx+1;
                end
                
            end
end
save(fullfile(base_folder, 'electrodes_info_names.mat'), 'electrodes_info')
