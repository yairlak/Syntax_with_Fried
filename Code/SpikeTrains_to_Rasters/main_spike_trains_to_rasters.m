
% Load settings and parameters
[settings, ~] = load_settings_params(settings);

% Choose which conditions to compare
[trials_info, settings] = get_condition_numbers(settings); 

% Get time points for all tokens of each condition for the paradigm log
 [trials_info, settings] = get_condition_times(trials_info, settings);

% Generate a raster for each condition, for all units, according to the condition time points and the spike trains of each unit
rasters = generate_rasters_from_spike_trains(trials_info, settings);

% Generate a figure for each unit with all conditions
figure_names = generate_raster_figures_singles(rasters, settings);