function run_visual_block(fid, stimuli_words, trialList, cumTrial, triggers, b, win, params)
audioStopTime   = -inf;


for trial=1:length(stimuli_words)
  cumTrial=cumTrial+1;
  stimulus=trialList(trial);

  
  %Echo status
  ['Block: ' num2str(b)]
  ['Trial: ' num2str(trial)]
  ['Stimulus: ' num2str(params.stimCode(stimulus)) ' = ' stimuli_words{stimulus}]
  

  % %%%%%%% DRAW FIXATION BEFORE SENTENCE (duration: params.fixation_duration)
  DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>+'], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');
  fixation_onset = Screen('Flip', win);  
  if triggers
      send_trigger(sio, dio, params, events, 'StartFixation', 0)
  end      
  while GetSecs-fixation_onset<params.fixation_duration  %Wait before trial
  end
    

  % %%%%%%% START RSVP
  for word = stimuli_words{stimulus}
      % %%%%%%% DRAW WORD, SEND TRIGGER AND WAIT SOA
      DrawFormattedText2(['<color=' params.font_color '><font=' params.font_name '><size=' num2str(params.font_size) '>' word{1}], 'win', win, 'sx', 'center', 'sy', 'center', 'xalign', 'center', 'yalign', 'center', 'xlayout', 'center');
      text_onset = Screen('Flip', win); % Word ON
      if triggers
          send_trigger(sio, dio, params, events, 'StartVisualWord', 0)
      end      
      while GetSecs-text_onset<params.stimulus_ontime
      end
      text_offset = Screen('Flip', win); % Word OFF
      if triggers
          send_trigger(sio, dio, params, events, 'EndVisualWord', 0)
      end
      while GetSecs-text_offset<params.stimulus_offtime
      end
      
      
      % %%%%%%% WRITE TO LOG
      fprintf(fid,[gettimestamp '\t'...
              'Stim\t' ...
              num2str(b) '\t' ...
              num2str(trial) '\t' ...
              num2str(params.stimCode(stimulus)) '\t' ...   %same code for '40Hz' and '40Hz-2'
              num2str(stimulus) '\t' ...   %different code for '40Hz' and '40Hz-2'
              params.shortenedWAVnames{stimulus} '\t' ...  %'40Hz-2.wav' becomes '40Hz'
              word{1} '\t' ...
              num2str(text_onset) '\t' ...
              num2str(text_offset) '\r\n' ...
              ]); % write to log file
      
      
  end % word
  
  % %%%%%% WAIT ISI before next sentences
  while GetSecs-text_offset+params.stimulus_offtime<params.ISI_visual 
  end
%     

end  %trial
%     
end