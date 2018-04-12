clear all; close all; clc
addpath('functions')

%% Define comparisons of interest:
% zSXXX ZSXXX phrase type
comparisons{1} = {11, 12};
comparison_name{1} = 'Num syllables';
condition_labels{1} = {'lessEqual_2','more_than_2'};
 
%% Run script
% Raw:
[settings, ~] = load_settings_params();
[custom_raw, custom_raw_smoothed, unit_names ] = create_raw_data(settings);
settings = [];

% Events:
for compar = 1:length(comparisons)
        custom_events = []; event_id = [];
        fprintf('%i. %s\n', compar, comparison_name{compar});
        settings = [];
        settings.conditions = comparisons{compar};
        settings.comparison_name = comparison_name{compar};
        settings.conditions_labels = condition_labels{compar};
        main_spike_trains_to_python
        event_id_all_comparisons{compar} = event_id;
        custom_events_all_comparisons{compar} = custom_events;
end
file_name = sprintf('raw_data_with_events_to_python_all_comparisons.mat');
save(fullfile('..','..','Output',file_name), 'custom_raw_smoothed', 'custom_events_all_comparisons', 'event_id_all_comparisons', 'unit_names', 'comparison_name')
