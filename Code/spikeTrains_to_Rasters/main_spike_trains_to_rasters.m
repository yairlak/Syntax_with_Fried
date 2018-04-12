
% Load settings and parameters:
[settings, ~] = load_settings_params(settings);

% Getting the relevant trial numbers and their corresponding timings.
% Results are summarized in the struct trials_info:
[trials_info, settings] = get_trial_info(settings);

% Generate a raster for each condition, for all units, according to the condition time points and the spike trains of each unit
[rasters, trials_info] = generate_rasters_from_spike_trains(trials_info, settings);

% PCA of words:
if run_PCA
    settings.window_size = 150;
    for l = 150:20:150
        settings.window_latency = l;
        single_words = analyze_single_word_responses(rasters, trials_info, settings, 2);
    end
   
end
% PCA of sentences:
end_of_sentence = analyze_end_of_sentence_response(rasters, trials_info, settings, 2);

% Generate a figure for each unit with all conditions:
if generate_rasters
    figure_names = generate_raster_figures_singles(rasters, trials_info, settings);
else
    figure_names = [];
end