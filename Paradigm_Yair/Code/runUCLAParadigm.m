%runUCLAParadigm.m
%This is the main script for the experiment, adapted to run using UCLA TTL
%hardware.
%Plays combination of 40Hz sound, sweep or one of two words

% uiwait(msgbox(sprintf('* Please  turn  off  WI-FI or diable Dropbox \n\n * Make  sure  that  in  Control  Panel  under  USB  Controller  the  baudrate  is  set  to  115200'),'Get Ready','warn'));

%Start by removing anything you had left over in the memory:
clear all; close all; clc
addpath('functions')
KbName('UnifyKeyNames')
[params, events] = getParamsUCLAParadigm();

%RightChannel='Ones';  %'Ones' implies all values are 1
RightChannel='Stim';  %'Stim' implies that we send the same stimulus to
%both audio output channels

%UCLA TTL settings
params.location='UCLA';  %options: 'UCLA' or 'TLVMC', affecting hardware to use for TTL
params.portA = 0;
params.portB = 1;


%#################################################################
% Send TTLs though the DAQ hardware interface
% triggers = questdlg('Send TTLs?','TTLs status','Yes (recording session)','No (just playing)','Yes (recording session)');
% if triggers(1) == 'Y', triggers = 1; else triggers = 0; end
% if ~triggers, uiwait(msgbox('TTLs  will  *NOT*  be  sent - are you sure you want to continue?','TTLs','modal')); end
%################################################################
triggers = 0;

%%
% %%%%%%% INITIALISING TTL HARDWARE
[sio, dio, DaqDOut, hwline, laststim] = initialize_TTL_hardware(triggers, params, events);

% Mark the beginning of the experiment with NINE consective '255' triggers separated by 0.1 sec
for i=1:9
    send_trigger(triggers, sio, dio, params, events, 'event255', 0.1)
end

% Running on PTB-3? Abort otherwise.
AssertOpenGL;
debugMode=0;
if debugMode
    params.numTrials=10;
    params.numBlocks=1;
    params.numSilents=0;
end

subses=['S' num2str(params.subject) '_' num2str(params.session)];


% %%%%%% OPEN LOG
timestamp = gettimestamp();
fid_log=createLogFileUCLAParadigm(params.defaultpath,subses,timestamp); % 10 fields
endlogline='\t\t\t\t\t\t\t\t\t\t\r\n';
copyfile(fullfile(params.defaultpath, 'runUCLAParadigm.m'),fullfile(params.defaultpath, '..', 'Logs', sprintf('runUCLAParadigm_%s_%s.m',timestamp,subses))); % copy code used for running to the log folder
copyfile(fullfile(params.defaultpath, 'getParamsUCLAParadigm.m'), fullfile(params.defaultpath, '..', 'Logs', sprintf('getParamsUCLAParadigm_%s_%s.m',timestamp,subses)))

% %%%%%% LOAD STIMULI
[stimuli_words, stimuli_wavs] = load_stimuli(params, timestamp, subses);
stimDur = cellfun(@(x) size(x, 1), stimuli_wavs, 'UniformOutput', false);  %in samples
% WAVTTL  = cellfun(ones(1,stimDur(i));

% %%%%%% INIT AUDIO
InitializePsychSound(1);
% pahandle = PsychPortAudio('Open', [], [], 0, params.freq, params.audioChannels, 0);
pahandle = PsychPortAudio('Open', 3, [], 2, params.freq, params.audioChannels, 0);

warning off
HideCursor

% %%%%%%% FOR DEBUG ONLY (COMMENT OUT IF NOT DEBUGGING)
PsychDebugWindowConfiguration([0],[0.5])
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --------------------------------------------

rect = get(0, 'ScreenSize');
rect = [0 0 rect(3:4)];
win = Screen('OpenWindow',0,[0 0 0],rect);


%%   ###############################################
%    MAIN LOOP
%    ------------------
%    ###############################################
    

% %%%%%% SHOW INTRO SLIDE
% intro_img_read = imread('../intro_slide.jpg');
% intro_img = Screen('MakeTexture', win, intro_img_read, [], [], [], [], 0);
% Screen('DrawTexture', win, intro_img, [], [], 0);
% Screen('Flip',win);

cumTrial=0;
for block = 1:6
    % %%%%%% WAIT FOR KEY PRESS
    DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>Press a key when ready'], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');    
    Screen('Flip',win);
    t_pressed = false;
    while ~t_pressed
        [~, ~, keyCode] = KbCheck;
        if any(keyCode)
            t_pressed = true;
    %     elseif keyCode(escKey)
    %         DisableKeysForKbCheck([]);
    %         Screen('CloseAll');
    %         return
        end
    end
    
    
    % %%%%%% BLOCK START: mark a new block with four 255 triggers separated 200ms from each other
    for i=1:4
        send_trigger(triggers, sio, dio, params, events, 'event255', 0.2)
    end
    
    % %%%%%% DRAW FIRST FIXATION 
    DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>+'], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');
    Screen('Flip', win);
    
    % %%%%%% BLOCK TYPE (odd blocks are visual; even auditory)
    if block == 1; grandStart = GetSecs; end
    
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
      run_visual_block(block, stimuli_words, VisualTrialOrder, fid_log, win, triggers, cumTrial, params, events)
    elseif strcmp(params.block_type, 'auditory')
      run_auditory_block(block, stimuli_wavs, AudioTrialOrder, fid_log, win, triggers, cumTrial, params, events, pahandle)
    end
end

%% %%%%%%% Close all
ShowCursor
Screen('CloseAll');
PsychPortAudio('Close', pahandle);
fprintf('Done\n')