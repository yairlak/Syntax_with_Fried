function run_auditory_block(block, stimuli_wavs, AudioTrialOrder, fid_log, win, triggers, cumTrial, params, events, pahandle)
audioStopTime   = -inf;


for trial=1:params.numTrials+params.numSilents
  
  % %%%%%% DRAW FIXATION
  DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>+'], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');
  fixation_onset = Screen('Flip', win);  
  
  cumTrial=cumTrial+1;
  stimulus=AudioTrialOrder(trial);
  clear wavedata;
  if (stimulus)
      wavedata(params.patientChannel,:) = stimuli_wavs{stimulus}(:,params.patientChannel);
      wavedata(params.TTLChannel,:) = wavedata(params.patientChannel,:);
  else
      wavedataslow(1:2,:) = zeros(2,params.freq*params.nullStimDur);  %Not actually loading null wav
  end
  %Echo status
  ['Block: ' num2str(block)]
  ['Trial: ' num2str(trial)]
  if (stimulus)
      ['Stimulus: ' num2str(stimulus) ' = ' params.WAVnames{stimulus}]
  else
      ['Stimulus: ' num2str(stimulus) ' = Null']
  end

  PsychPortAudio('FillBuffer', pahandle, wavedata);
  while GetSecs-fixation_onset<params.fixation_duration_audio  %Wait before trial
  end
  fixation_offset = Screen('Flip', win);
  % %%%%%%% WRITE TO LOG
    fprintf(fid_log,[gettimestamp '\t'...
          'Fix\t' ...
          num2str(block) '\t' ...
          num2str(trial) '\t' ...
          num2str(0) '\t' ... % Stimulus serial number in original stimulus text file
          '' '\t' ...  %
          '+' '\t' ...
          num2str(fixation_onset) '\t' ...
          num2str(fixation_offset) '\r\n' ...
          ]); % write to log file
      
  

  % %%%%%%% START AUDIO AND SEND TRIGGER AT START AND END
  audioOnset = PsychPortAudio('Start', pahandle, 1, 0, 1); % it takes ~15ms to start the sound
  if triggers
      send_trigger(triggers, sio, dio, params, events, 'StartAudio', 0)
  end
  % Wait for playback to stop:
  [~, ~, ~, audioStopTime]=PsychPortAudio('Stop', pahandle,1);
  if triggers
      send_trigger(triggers, sio, dio, params, events, 'EndAudio', 0)
  end

  % %%%%%%% CLEAR-UP (buffer and screen)
  PsychPortAudio('DeleteBuffer',[],1); % clear the buffer
  fixation_offset = Screen('Flip', win); % Remove fixation +
  
  % %%%%%%% WRITE TO LOG
  fprintf(fid_log,[gettimestamp '\t'...
      'Stim\t' ...
      num2str(block) '\t' ...
      num2str(trial) '\t' ...
      num2str(stimulus) '\t' ...   %different code for '40Hz' and '40Hz-2'
      params.shortenedWAVnames{stimulus} '\t' ...  %'40Hz-2.wav' becomes '40Hz'
      params.WAVnames{stimulus} '\t' ...
      num2str(audioOnset) '\t' ...
      num2str(audioStopTime) '\r\n' ...
      ]); % write to log file

  
  % %%%%%% WAIT ISI
    while GetSecs-audioStopTime<params.ISI_audio %Wait before showing next sentencesw
    end


end  %trial
%     
end