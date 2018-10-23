function run_auditory_block(fid, win, RightChannel, WAVstimulus, trialList, cumTrial, triggers, location, b, pahandle, params)
audioStopTime   = -inf;


for trial=1:params.numTrials+params.numSilents
  cumTrial=cumTrial+1;
  stimulus=trialList(trial);   %different value for e.g. 40Hz-2 and 40Hz

  DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>+'], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');
  fixation_onset = Screen('Flip', win);  
  
  clear wavedata;
  if (stimulus)
      wavedata(params.patientChannel,:) = WAVstimulus{stimulus}(:,params.patientChannel);
      if RightChannel=='Ones'
          wavedata(params.TTLChannel,:) = WAVTTL{stimulus};
      elseif RightChannel=='Stim'
          wavedata(params.TTLChannel,:) = wavedata(params.patientChannel,:);
      else
          error('incorrect RightChannel setting');
      end
  else
      wavedata(1:2,:) = zeros(2,params.freq*params.nullStimDur);  %Not actually loading null wav
  end
  PsychPortAudio('FillBuffer', pahandle, wavedata);
  while GetSecs-fixation_onset<params.fixation_duration_audio  %Wait before trial
  end


  %Echo status
  ['Block: ' num2str(b)]
  ['Trial: ' num2str(trial)]
  if (stimulus)
      ['Stimulus: ' num2str(params.stimCode(stimulus)) ' = ' params.WAVnames{stimulus}]
  else
      ['Stimulus: ' num2str(stimulus) ' = Null']
  end


  % Start audio playback immediately (0) and wait for the playback to start, return onset timestamp.
  audioOnset = PsychPortAudio('Start', pahandle, 1, 0, 1); % it takes ~15ms to start the sound
  if triggers
      if stimulus
          if triggers && strcmp(location,'TLVMC'), fwrite(sio,eventStartAudio+params.stimCode(stimulus)); WaitSecs(ttlwait); fwrite(sio,eventreset); end
          if triggers && strcmp(location,'UCLA'), DaqDOut(dio,portA,eventStartAudio+params.stimCode(stimulus)); WaitSecs(ttlwait); DaqDOut(dio,portA,eventreset); end
      else
          %send 'Null' code
          if triggers && strcmp(location,'TLVMC'), fwrite(sio,eventStartAudio); WaitSecs(ttlwait); fwrite(sio,eventreset); end
          if triggers && strcmp(location,'UCLA'), DaqDOut(dio,portA,eventStartAudio); WaitSecs(ttlwait); DaqDOut(dio,portA,eventreset); end
      end
  end

  % Wait for playback to stop:
  [~, ~, ~, audioStopTime]=PsychPortAudio('Stop', pahandle,1);
  if triggers
      if stimulus
          if triggers && strcmp(location,'TLVMC'), fwrite(sio,eventEndAudio+params.stimCode(stimulus)); WaitSecs(ttlwait); fwrite(sio,eventreset); end
          if triggers && strcmp(location,'UCLA'), DaqDOut(dio,portA,eventEndAudio+params.stimCode(stimulus)); WaitSecs(ttlwait); DaqDOut(dio,portA,eventreset); end
      else
          if triggers && strcmp(location,'TLVMC'), fwrite(sio,eventEndAudio); WaitSecs(ttlwait); fwrite(sio,eventreset); end
          if triggers && strcmp(location,'UCLA'), DaqDOut(dio,portA,eventEndAudio); WaitSecs(ttlwait); DaqDOut(dio,portA,eventreset); end
      end          
  end

  PsychPortAudio('DeleteBuffer',[],1); % clear the buffer
  fixation_offset = Screen('Flip', win); % Remove fixation +
  
  %write to CVS logfile
  if (stimulus)
      fprintf(fid,[gettimestamp '\t'...
          'Stim\t' ...
          num2str(b) '\t' ...
          num2str(trial) '\t' ...
          num2str(params.stimCode(stimulus)) '\t' ...   %same code for '40Hz' and '40Hz-2'
          num2str(stimulus) '\t' ...   %different code for '40Hz' and '40Hz-2'
          params.shortenedWAVnames{stimulus} '\t' ...  %'40Hz-2.wav' becomes '40Hz'
          params.WAVnames{stimulus} '\t' ...
          num2str(audioOnset) '\t' ...
          num2str(audioStopTime) '\r\n' ...
          ]); % write to log file
  else
      fprintf(fid,[gettimestamp '\t'...
          'Stim\t' ...
          num2str(b) '\t' ...
          num2str(trial) '\t' ...
          num2str(stimulus) '\t' ...   %stim code
          num2str(stimulus) '\t' ...
          'Null' '\t' ...
          'Null' '\t' ...
          num2str(audioOnset) '\t' ...
          num2str(audioStopTime) '\r\n' ...
          ]); % write to log file
  end
  
  while GetSecs-audioStopTime<params.ISI_audio %Wait before showing next sentencesw
  end


end  %trial
%     
end