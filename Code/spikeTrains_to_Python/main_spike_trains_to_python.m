% A script to generate rasters from spike trains, given a condition list
% clear all; close all; clc
addpath('functions')

%%
% Load settings and parameters
[settings, ~] = load_settings_params(settings);

% Getting the relevant trial numbers and their corresponding timings.
% Results are summarized in the struct trials_info:
[trials_info, settings] = get_trial_info(settings);

% Create Epochs and Events objects
custom_events = create_epochs_and_events(trials_info, settings);