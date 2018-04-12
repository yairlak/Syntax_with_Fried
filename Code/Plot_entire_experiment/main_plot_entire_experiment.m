clear all; close all; clc
addpath('functions')

%%
% Load settings and parameters
[settings, ~] = load_settings_params();

% Load spike data from all units
[spike_data_all_units, unit_names]  = load_spike_data(settings);

% Load stimulus onsets, and extract presentation times of the first words
[trial_times,  ~ ] = get_trial_times(settings);

% Plot spike trains from all units for the entire experimental duration
plot_all_units_entire_experiment(spike_data_all_units, unit_names, trial_times, settings)
