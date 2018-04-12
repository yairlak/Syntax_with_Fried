function rasters = generate_rasters_from_spike_trains(trials_info, settings)

all_units = dir(fullfile(settings.path2data, 'CSC*.mat'));

for unit = 1:length(all_units)
    curr_file_name = all_units(unit).name;
    curr_data = load(fullfile(settings.path2data, curr_file_name));
    curr_spike_train = curr_data.spike_times_sec * 1000; %sec to ms
    unit_name = curr_file_name(1:strfind(curr_file_name, '.')-1);
    
    %% Button press
    if settings.generate_key_press_rasters
        curr_raster = [];spike_times_all_trials=[];
        for trial = 1:length(trials_info.trial_times_button_press)
            curr_trial_timing = trials_info.trial_times_button_press(trial);
            curr_trial_timing = curr_trial_timing/1e3; % from microsec to ms
            relative_to_curr_trial = curr_spike_train - curr_trial_timing;
            IX_in_window = relative_to_curr_trial > -1*settings.duration_before_stimulus_onset & ...
                                                relative_to_curr_trial < settings.duration_after_stimulus_onset;
            curr_spike_times = relative_to_curr_trial(IX_in_window);
            spike_times_all_trials{trial} = curr_spike_times;
            curr_spike_times = round(curr_spike_times); % Omit rounding in later versions
            curr_trial_spikes = zeros(1,  settings.duration_before_stimulus_onset+ settings.duration_after_stimulus_onset+1);
            curr_trial_spikes(curr_spike_times + settings.duration_before_stimulus_onset+1) = 1;
            curr_raster(trial, :) = curr_trial_spikes;
        end
        rasters.(unit_name).button_press.matrix = curr_raster;
        rasters.(unit_name).button_press.spike_times = spike_times_all_trials;
    end
    
    %% Conditions
    % For each condition, extract the spikes
    if settings.generate_condition_rasters
            for cnd = 1:length(trials_info.trial_times_per_condition)
                cnd_name = settings.conditions_labels{cnd}; 
                curr_condition_trials_timings = trials_info.trial_times_per_condition{cnd};
                curr_raster = [];spike_times_all_trials=[];
                for trial = 1:length(curr_condition_trials_timings)
                    curr_trial_timing = curr_condition_trials_timings(trial);
                    curr_trial_timing = curr_trial_timing/1e3; % from microsec to ms
                    relative_to_curr_trial = curr_spike_train - curr_trial_timing;
                    IX_in_window = relative_to_curr_trial > -1*settings.duration_before_stimulus_onset & ...
                                                        relative_to_curr_trial < settings.duration_after_stimulus_onset;
                    curr_spike_times = relative_to_curr_trial(IX_in_window);
                    spike_times_all_trials{trial} = curr_spike_times;
                    curr_spike_times = round(curr_spike_times); % Omit rounding
                    curr_trial_spikes = zeros(1,  settings.duration_before_stimulus_onset+ settings.duration_after_stimulus_onset+1);
                    curr_trial_spikes(curr_spike_times + settings.duration_before_stimulus_onset+1) = 1;
                    curr_raster(trial, :) = curr_trial_spikes;

                end
                rasters.(unit_name).(cnd_name).matrix = curr_raster;
                rasters.(unit_name).(cnd_name).spike_times = spike_times_all_trials;
            end
    else
        rasters = [];
    end

end

% Save
if strcmp(settings.block_name, 'sentences')
    settings_fields = {'patient', 'comparison_name', 'block_name', 'lock_to_word'};
else
    settings_fields = {'patient', 'comparison_name', 'block_name'};
end
params = []; params_fields = [];
file_name = get_file_name_curr_run(settings, params, settings_fields, params_fields);
file_name = ['raster_all_units_' file_name '.mat'];
save(fullfile('..', '..', 'Output', file_name))

end