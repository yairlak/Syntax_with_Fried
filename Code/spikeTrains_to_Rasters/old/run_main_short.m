clear all; close all; clc

%%
settings.conditions = [];
settings.comparison_name = 'All trials';
settings.conditions_labels = {'all_trials'};

%%
patients = {'ArM01', 'En_01'};
patients = {'En_01'};
block_names = {'sentences'};

for p = 1:length(patients)
    settings.patient = patients{p};
    for bn = 1:length(block_names)
        settings.block_name = block_names{bn};
        main_spike_trains_to_rasters
    end
end
