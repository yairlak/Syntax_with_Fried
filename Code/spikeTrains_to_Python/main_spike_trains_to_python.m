% A script to generate rasters from spike trains, given a condition list
% clear all; close all; clc
addpath('functions')

%%
% Load settings and parameters
[settings, ~] = load_settings_params(settings);

<<<<<<< HEAD
% Getting the relevant trial numbers and their corresponding timings.
% Results are summarized in the struct trials_info:
[trials_info, settings] = get_trial_info(settings);
=======
% Choose which conditions to compare
[trials_info, settings] = get_condition_numbers(settings);

% Get time points for all tokens of each condition for the paradigm log
trials_info = get_condition_times(trials_info, settings);
>>>>>>> 5b9b039709819b6943ba2d6fe6a2cb30b8113304

% Create Epochs and Events objects
custom_events = create_epochs_and_events(trials_info, settings);