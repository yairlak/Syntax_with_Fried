clear all; close all; clc
addpath('functions')

%% Define comparisons of interest:
settings.hospital = 'UCLA';
patients = {'patient_479'};
% block_names = {'words', 'words_press', 'nonwords', 'nonwords_press', 'sentences'};
run_names = {'sentences'};
settings.blocks = [1:2]; % For example, with En_02 there were 6 blocks: visual #1,3,5 and auditory 2,4,6.
blocks_str = num2str(settings.blocks);
blocks_str = strrep(blocks_str,' ','');
settings.block_type = 'mixed'; %e.g., 'visual', 'audio', 'mixed'
comparison_list = [1:6];%,10,12,18]; % Comparisons in file to run. If empty, then run all.

settings.block_name = run_names{1};
settings.patient = patients{1};
file_name = sprintf('Comparisons %s %s %s.xlsx', settings.hospital, settings.patient, settings.block_name);
[~, comparison_file, ~] = xlsread(fullfile('..', '..', 'Paradigm', file_name));
if isempty(comparison_list)
    comparison_list = 1:size(comparison_file, 1)-1;
end

%% Run script
% Raw:
[settings, ~] = load_settings_params(settings);
[custom_raw, custom_raw_smoothed, unit_names, settings ] = create_raw_data(settings);
lock_to_word_array = [];
% Events:
for comp = (comparison_list+1)
        % Comparison Info:
        settings.conditions = eval(comparison_file{comp, 2});
        if ~isempty(comparison_file{comp, 6})
            settings.conditions_union = eval(comparison_file{comp, 6});
            if length(settings.conditions) ~= length(settings.conditions_union)
                error('Check Excel comparison files. Make sure Column C and G have the same length')
            end
        else
            settings.conditions_union = [];
        end
        settings.comparison_name = comparison_file{comp, 1};
        if ~isempty(comparison_file{comp, 3})
            settings.conditions_labels = eval(comparison_file{comp, 3});
        end
        settings.lock_to_word = comparison_file{comp, 4};
        settings.comparison_comments = comparison_file{comp, 5};
        
        fprintf('PATIENT %s, BLOCK %s, COMPARISON %s\n', settings.patient, settings.block_name, settings.comparison_name);
        custom_events = []; event_id = [];
        main_spike_trains_to_python
        event_id = settings.conditions_labels;
        event_id_all_comparisons{comp-1} = event_id;
        custom_events_all_comparisons{comp-1} = custom_events;
        comparison_name{comp-1} = comparison_file{comp, 1};
end

file_name = sprintf('raw_data_with_events_to_python_all_comparisons_%s_%s_blocks_%s.mat', settings.patient, settings.block_name, blocks_str);
save(fullfile('..','..','Output',file_name), 'custom_raw_smoothed', 'custom_events_all_comparisons', 'event_id_all_comparisons', 'unit_names', 'comparison_name', 'settings', 'lock_to_word_array')
