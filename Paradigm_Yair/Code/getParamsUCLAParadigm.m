function [params, events] = getParamsUCLAParadigm()
%function params = getParams
%This function makes the struct that holds the parameters for the presentation of the stimuli and such.

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

params.jitter = 0;    %Seperation of start times is SOA +/- Jitter with uniform random distribution. set to zero if want no jitter in stimuli times. 

params.freq=44100;
params.vol=1;
params.audioChannels=2;
params.fixation_duration_audio = 0.6;
params.ISI_audio = 1;

params.font_size = 50; % Fontsize for words presented at the screen center
params.font_name = 'Courier New';
params.font_color = 'ffffff';
params.fixation_duration = 0.6; %
params.stimulus_ontime = 0.25; % Duration of each word
params.stimulus_offtime = 0.25; % Duration of black between stimuli
params.SOA_visual = params.stimulus_ontime + params.stimulus_offtime;
params.ISI_visual = 1; % from end of last trial to beginning of first trial

params.numPerWAV = 1;       %number of trials for each wave per block
params.numSilents = 0;  %Number of silent or null trials per block
params.nullStimDur=0.5; % 500 ms    %length of null stimulus
%params.SOA=1.5;  %deprecated: average time from start of stim to start of next
params.stimSeparation=1;    %average time separating stimuli (end of one to start of next)
params.WAVnamesStruct=dir(fullfile(params.WAVpath, '*.wav'));
params.numWAVs = size(params.WAVnamesStruct,1);
for i =1:params.numWAVs
    params.WAVnames{i} = params.WAVnamesStruct(i).name;
end

%remove number suffix from wav filenames, and assign stimCodes. Repeated stimuli are indicated by '-' and a number before '.wav':
for i =1:params.numWAVs
    params.shortenedWAVnames{i} = params.WAVnames{i}(1:end-4);   %remove '.wav'
end
uniqueWAVnames = unique(params.shortenedWAVnames);

params.text_filename = dir(fullfile(params.Visualpath, 'stimuli_*.txt'));
params.text_filename = params.text_filename(1).name;


params.numTrials = params.numWAVs * params.numPerWAV;

params.patientChannel=1;  %audio channel number to patient
params.TTLChannel=2;      %channel number for square wave TTL to show when stimulus is running

subject = inputdlg({'Enter subject number'},...
    'Subject Number',1,{''});

session = inputdlg({'Enter session number'},...
    'Subject Number',1,{''});

%User defined params:
params.subject=subject{1};

params.session=str2double(session);

events.StartVisualTrial = 100;
events.EndVisualTrial = 101;
events.StartVisualWord = 110;
events.EndVisualWord = 111;

events.StartAudio = 200;
events.EndAudio   = 201;

events.StartFixation = 100;
events.EndFixation = 110;

events.event255        = 255;
events.eventreset      = 0;
events.ttlwait         = 0.01;
events.audioOnset      = 0;
events.eventResp       = 45;


end