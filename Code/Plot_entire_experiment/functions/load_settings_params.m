function [settings, params] = load_settings_params(settings)
    % Params
    params = [];
    settings.units = 31:40;%For ALL units set to 1:47 
     settings.units = 1:10;
     
    %% Settings
    settings.path2data = fullfile('..', '..', 'Data', 'Patients', 'En_01');
    settings.patient = 'ArM01';
    settings.patient = 'En_01';
    settings.run_type_file = 'block2_sentences_events_list.log';
    
    %% Visualization
    % Rasters:
    settings.step_gca = 250; % Step of xtick labels in rasters
    settings.line_size = 0.4; % Rasters' vertical-line size (less than 1, which is the vertical distance between trials)
end