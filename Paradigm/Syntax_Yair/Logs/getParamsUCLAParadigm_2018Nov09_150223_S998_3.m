function [params, events] = getParamsUCLAParadigm()
%function params = getParams
%This function makes the struct that holds the parameters for the presentation of the stimuli and such.

%% %%%%%%% PATHS
params.path2intro_slide = '../Stimuli/instructions_sentences.png';
if ismac || isunix %comp == 'h'
    params.defaultpath = '~/Projects/single_unit_syntax/Paradigm_Yair/Code';
    params.WAVpath = fullfile('..', 'Stimuli', 'audio');
    params.Visualpath = fullfile('..', 'Stimuli', 'visual');
    params.sio = '/dev/tty.usbserial';
elseif ispc % strcmp(comp,'l')
    params.defaultpath = '~/Projects/single_unit_syntax/Paradigm_Yair/Code';
    params.WAVpath = fullfile(params.defaultpath, 'WAVs');
    params.Visualpath = fullfile('..', 'Stimuli', 'visual');
    params.sio='COM1';
end

%% %%%%%%% FILENAMES STIMULI
params.text_filename = 'sentences_Eng_debug.txt';
params.WAVnamesStruct=dir(fullfile(params.WAVpath, '*.wav'));
params.numTrialsAudioBlock = size(params.WAVnamesStruct,1);
for i =1:params.numTrialsAudioBlock
    params.WAVnames{i} = params.WAVnamesStruct(i).name;
end

%% %%%%%%% AUDIO params
params.freq=44100;
params.vol=1;
params.audioChannels=2;

params.patientChannel=1;  %audio channel number to patient
params.TTLChannel=2;      %channel number for square wave TTL to show when stimulus is running


%% %%%%%%% TEXT params
params.font_size = 50; % Fontsize for words presented at the screen center
params.font_name = 'Courier New';
params.font_color = 'ffffff';

%% %%%%%%% TIMING params
% VISUAL BLOCK
params.fixation_duration_visual_block = 0.6; %
params.stimulus_ontime = 0.25; % Duration of each word
params.stimulus_offtime = 0.25; % Duration of black between stimuli
params.SOA_visual = params.stimulus_ontime + params.stimulus_offtime;
params.ISI_visual = 1; % from end of last trial to beginning of first trial

% AUDIO BLOCK
params.fixation_duration_audio_block = 0.6;
params.ISI_audio = 1;

%% EVENTS NUMBERS (TRIGGERS)
% FIXATION
events.StartFixation = 10;
events.EndFixation = 11;

% VISUAL BLOCK
events.StartVisualWord = 20;
events.EndVisualWord = 21;

% AUDIO BLOCK
events.StartAudio = 30;
events.EndAudio   = 31;

% KEY PRESS
events.PressKey = 50;

% MISC
events.event255        = 255;
events.eventreset      = 0;
events.ttlwait         = 0.01;
events.audioOnset      = 0;
events.eventResp       = 145;

%% SUBJECT AND SESSION NUMBERS
subject = inputdlg({'Enter subject number'},...
    'Subject Number',1,{''});
params.subject=subject{1};

session = inputdlg({'Enter session number'},...
    'Subject Number',1,{''});
params.session=str2double(session);

end