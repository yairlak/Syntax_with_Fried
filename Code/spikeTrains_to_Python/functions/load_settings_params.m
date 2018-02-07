function [settings, params] = load_settings_params(settings)
    % Params
    params = [];
    
    %% Settings
    % Path
    settings.path2data = fullfile('..', '..', 'Data', 'UCLA', 'patient_479'); 
    % Log file name:
%     settings.run_type_file = 'new_mouse_recording_in_cheetah_clock_part1.log';
    % Feature codes file location:
    features_codes_file = sprintf('features %s %s %s.xlsx',  settings.hospital, settings.patient,settings.block_name);
    settings.feautre_codes_file = fullfile('..','..','Paradigm', features_codes_file);    
    
    % Preferences
%     settings.lock_to_word = 'last'; %'first'/'last' (English sentences have varying lengths)
    settings.generate_key_press_rasters = false;
    settings.generate_condition_rasters = true;
    
    % Raster visualization
    settings.duration_before_stimulus_onset = 3500; % [ms] POSITIVE!
    settings.duration_after_stimulus_onset = 3500; % [ms]
    settings.SOA = 350; %[ms] (used to draw vertical lines for various stimuli on the same rasters)
    settings.step_gca = 500; % Step of xtick labels in rasters
    settings.line_size = 0.4; % Rasters' vertical-line size (less than 1, which is the vertical distance between trials)
    settings.PSTH_bin_size = 100; % [ms]
    settings.PSTH_ylim = 22; % [Hz]

end
 
