function run_visual_block(handles, block, stimuli_words, VisualTrialOrder, fid_log, triggers, cumTrial, params, events)
% %%%%%% WAIT FOR KEY PRESS
if block>1
    DrawFormattedText(handles.win, 'Press any key...', 'center', 'center', handles.white);
    Screen('Flip',handles.win);
    wait_for_key_press()   
end

% %%%%%% BLOCK START: mark a new block with four 255 triggers separated 200ms from each other
block_start = GetSecs;
for i=1:4
    send_trigger(triggers, handles, params, events, 'event255', 0.2)
end
% %%%%%%% WRITE TO LOG
fprintf(fid_log,['BlockStart\t' ...
      num2str(block) '\t' ...
      num2str(0) '\t' ...
      num2str(0) '\t' ... % Stimulus serial number in original stimulus text file
      '' '\t' ...  %
      '-' '\t' ...
      num2str(block_start) '\t' ...
      '' '\r\n' ...
      ]); % write to log file

for trial=1:length(stimuli_words)
  [~, ~, keyCode] = KbCheck;
  if keyCode('ESCAPE')
    DisableKeysForKbCheck([]);
    Screen('CloseAll');
    return
  end
  cumTrial=cumTrial+1;
  stimulus=VisualTrialOrder(trial);
  fprintf('Block %i, trial %i\n', block, trial)
  

  % %%%%%%% DRAW FIXATION BEFORE SENTENCE (duration: params.fixation_duration)
  DrawFormattedText(handles.win, '+', 'center', 'center', handles.white);
  fixation_onset = Screen('Flip', handles.win);
  if triggers
      send_trigger(triggers, handles, params, events, 'StartFixation', 0)
  end
  [pressed, firstPress]=KbQueueCheck; % Collect keyboard events since KbQueueStart was invoked
  WaitSecs('UntilTime', fixation_onset + params.fixation_duration_visual_block); %Wait before trial
  fixation_offset = Screen('Flip', handles.win);
  
  % %%%%%%% WRITE TO LOG
  fprintf(fid_log,['Fix\t' ...
          num2str(block) '\t' ...
          num2str(trial) '\t' ...
          num2str(0) '\t' ... % Stimulus serial number in original stimulus text file
          '' '\t' ...  %
          '+' '\t' ...
          num2str(fixation_onset) '\r\n' ...
          ]); % write to log file

    
    

  % %%%%%%% START RSVP for current sentence
  word_cnt = 0;
  for word = stimuli_words{stimulus}
      word_cnt = word_cnt + 1;
      % TEXT ON
      DrawFormattedText(handles.win, word{1}, 'center', 'center', handles.white);
      text_onset = Screen('Flip', handles.win); % Word ON
      if triggers
          send_trigger(triggers, handles, params, events, 'StartVisualWord', 0)
      end
      if pressed
          if triggers
               send_trigger(triggers, handles, params, events, 'PressKey', 0)
          end
      end
      WaitSecs('UntilTime', text_onset + params.stimulus_ontime);
      % TEXT OFF
      text_offset = Screen('Flip', handles.win); % Word OFF
      if triggers
          send_trigger(triggers, handles, params, events, 'EndVisualWord', 0)
      end
      if pressed
            if firstPress(KbName('l')) || firstPress(KbName('L'))
                
                fprintf(fid_log,['KeyPress\t' ...
                  num2str(block) '\t' ...
                  num2str(trial) '\t' ...
                  num2str(stimulus) '\t' ... % Stimulus serial number in original stimulus text file
                  '\t' ...  %
                  '\t' ...
                  num2str(firstPress(KbName('l'))) '\t' ...
                  '\r\n' ...
                  ]); % write to log file
            end
            if firstPress(KbName('escape'))
                error('Escape key was pressed')
            end
      end
      % WRITE TO LOG
      fprintf(fid_log,['StimVisualOn\t' ...
              num2str(block) '\t' ...
              num2str(trial) '\t' ...
              num2str(stimulus) '\t' ... % Stimulus serial number in original stimulus text file
              num2str(word_cnt) '\t' ...  %
              word{1} '\t' ...
              num2str(text_onset) '\r\n' ...
              ]); % write to log file
      fprintf(fid_log,['StimVisualOff\t' ...
              num2str(block) '\t' ...
              num2str(trial) '\t' ...
              num2str(stimulus) '\t' ... % Stimulus serial number in original stimulus text file
              num2str(word_cnt) '\t' ...  %
              '\t' ...
              num2str(text_offset) '\r\n' ...
              ]); % write to log file
        

      WaitSecs('UntilTime', text_offset + params.stimulus_offtime);
      
      
  end % word
  
  % %%%%%% WAIT ISI before next sentences
  WaitSecs('UntilTime', text_offset + params.stimulus_offtime + params.ISI_visual);
      
  
end  %trial
%     
end