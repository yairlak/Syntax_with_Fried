%% 
% This is the main script for the experiment
% ------------------------------------------------
clear all; close all; clc
debug_mode = 0;

%% INITIALIZATION
addpath('functions')
KbName('UnifyKeyNames')
[params, events] = getParamsUCLAParadigm();
rng(str2double(params.subject)*params.session);

%UCLA TTL settings
params.location='UCLA';  %options: 'UCLA' or 'TLVMC', affecting hardware to use for TTL
params.portA = 0;
params.portB = 1;

% Running on PTB-3? Abort otherwise.
AssertOpenGL;

%% TRIGGERS
%#################################################################
% Send TTLs though the DAQ hardware interface
triggers = questdlg('Send TTLs?','TTLs status','Yes (recording session)','No (just playing)','Yes (recording session)');
if triggers(1) == 'Y', triggers = 1; else triggers = 0; end
if ~triggers, uiwait(msgbox('TTLs  will  *NOT*  be  sent - are you sure you want to continue?','TTLs','modal')); end
%################################################################
%triggers = 0;
handles = initialize_TTL_hardware(triggers, params, events);

%% LOAD LOG, STIMULI, PTB handles.
if triggers
    for i=1:9 % Mark the beginning of the experiment with NINE consective '255' triggers separated by 0.1 sec
        send_trigger(triggers, handles, params, events, 'event255', 0.1)
    end
end
fid_log=createLogFileUCLAParadigm(params); % OPEN LOG
[stimuli_words, stimuli_wavs] = load_stimuli(params); % LOAD STIMULI
stimDur = cellfun(@(x) size(x, 1), stimuli_wavs, 'UniformOutput', false);  %in samples
handles = Initialize_PTB_devices(params, handles, debug_mode);
warning off; HideCursor


%% START EXPERIMENT
try
    present_intro_slide(params, handles);
    KbStrokeWait;
    KbQueueStart;
    cumTrial=0;
    % PRESENT LONG FIXATION ONLY AT THE BEGINING
    DrawFormattedText(handles.win, '+', 'center', 'center', handles.white);
    Screen('Flip', handles.win);
    WaitSecs(1.5); %Wait before experiment start
    % START LOOP OVER BLOCKS
    for block = 1:6
        % %%%%%% BLOCK TYPE (odd blocks are visual; even auditory)
        if block == 1
            % %%%%%%% WRITE TO LOG
              fprintf(fid_log,['GrandStart\t' ...
              '\t' ...
              '\t' ...
              '\t' ... % Stimulus serial number in original stimulus text file
              '\t' ...  %
              '---' '\t' ...
              num2str(GetSecs) '\t' ...
              '' '\r\n' ...
              ]); % write to log file
        end
  
        if mod(block, 2) == 0
            params.block_type = 'auditory';
        else
            params.block_type = 'visual';
        end
        % %%%%%%% RANDOMIZE TRIAL LIST
        AudioTrialOrder=randperm(length(stimuli_wavs));
        VisualTrialOrder=randperm(length(stimuli_words));

        % %%%%%% LOOP OVER STIMULI
        if strcmp(params.block_type, 'visual')
          run_visual_block(handles, block, stimuli_words, VisualTrialOrder, fid_log, triggers, cumTrial, params, events)
        elseif strcmp(params.block_type, 'auditory')
          run_auditory_block(handles, block, stimuli_wavs, AudioTrialOrder, fid_log, triggers, cumTrial, params, events)
        end
    end
catch
    sca
    PsychPortAudio('Close', handles.pahandle);
    psychrethrow(psychlasterror);
    KbQueueRelease;
    fprintf('Error occured\n')
end

%% %%%%%%% CLOSE ALL - END EXPERIMENT
fprintf('Done\n')
KbQueueRelease;
sca