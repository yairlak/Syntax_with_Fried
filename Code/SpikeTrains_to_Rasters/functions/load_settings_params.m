function [settings, params] = load_settings_params(settings)
    % Params
    params = [];
    
    %% Settings
%     settings.patient = 'En_01';
%     settings.block_name = 'words_press';
%     
    % Path
    settings.path2data = fullfile('..', '..', 'Data', 'Patients', settings.patient, settings.block_name); 
    % Log file name:
    settings.run_type_file = 'mouse_recording_in_cheetah_clock.log';
    % Feature codes file location:
    features_codes_file = sprintf('features %s %s.xlsx',  settings.patient,settings.block_name);
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
    
%     settings.conditions = {[5,6], [4,6], [1,6,8,13], [1,7,8,13]};% 
%     settings.conditions_labels = {'zSXXX', 'ZSXXX', 'DSNEX' ,'DVNEX'};
%     settings.conditions = {20, 21};% first/second half
%     settings.conditions_labels = {'First', 'Second'}; %
%      settings.conditions = {[1, 6, 8], [1,6,9], [1,6,11]};% DSN, DSP, DSH
%      settings.conditions_labels = {'N__ADJ', 'N__NP', 'SV', 'VS'}; %
%     settings.conditions = {[1,6,8,12,19]};% first/second half
%     settings.conditions_labels = {'DSNAM'}; %
%     settings.conditions = {[1,6,11,13]};% first/second half
%     settings.conditions_labels = {'DSHEX'}; %
% 
% 
    
% (1) Declarative (D)	
% (2) WH-question (W)
% (3) NP+AP (G)	
% (4) N + NP (Z)
% (5) N + ADJ (z)
% (6) S
% (7) V
% (8) N	
% (9) P
% (10) R
% (11) H
% (12) A
% (13) E
% (14) C
% (15) T
% (16) t
% (17) K
% (18) O
% (19) M    
    
end

% zSXXX ZSXXX
% phrase type
% 
% zSXXX GSNXX
% phrase vs sentence
% 
% GSNXX DSNEX
% nominal vs verbal sentence
% 
% DSHEX DSHAX
% argument structure unacc vs unerg
% 
% DSHTK DSHCK
% argument structure transitive vs causative
% 
% DSHEX WSXEX
% declarative vs question
% 
% DSNEX DVNEX
% SV vs. VS
% 
% WSRTX WSXEX
% subject vs object question
% 
% DVNEX DSXAM
% VS with and without movement
% 
% DSNEX DSPEX+DSHEX
% pronoun vs full NP subject: unerg
% 
% DSNAM % DSPAM+DSHAM
% pronoun vs full NP subject: unacc
% 
% DSNTK % DSHTK+DSPTK
% pronoun vs full NP subject: transitive
 