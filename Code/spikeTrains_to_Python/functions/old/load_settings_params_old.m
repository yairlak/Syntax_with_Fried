function [settings, params] = load_settings_params(settings)
    % Params
    params = [];
    
    %% Settings
    settings.patient = 'En_01';
    settings.block_name = 'words_press';
    settings.path2data = fullfile('..', '..', 'Data', 'Patients', settings.patient, settings.block_name); 
    % Log file
    settings.run_type_file = 'block2_sentences_events_list.log';
%     settings.duration_before_stimulus_onset = 1000; % [ms]
%     settings.duration_after_stimulus_onset = 1500; % [ms]
%     settings.SOA = 350; %[ms]
%     % Condition info:
    
    
end

 