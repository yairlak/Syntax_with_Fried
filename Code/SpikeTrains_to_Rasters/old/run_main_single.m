clear all; close all; clc
addpath('functions')
%%
% settings.conditions = {3};
% settings.comparison_name = 'Num of Letters';
% settings.conditions_labels = {};

settings.conditions = {7,8};
settings.comparison_name = 'Morphological complexity';
settings.conditions_labels = {'simple', 'complex'};

% settings.conditions = {6, 12};
% settings.comparison_name = 'Num of syllables';
% settings.conditions_labels = {'Syl_1_2', 'Syl_3_4_5'};

%%
patients = {'En_01'};
block_names = {'words'};

for p = 1:length(patients)
    settings.patient = patients{p};
    for bn = 1:length(block_names)
        settings.block_name = block_names{bn};
        main_spike_trains_to_rasters
    end
end
