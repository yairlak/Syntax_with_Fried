function [trials_info, settings] = get_trial_info(settings)

trials_info.category_position = [];
trials_info.key_was_pressed_after.sentence = [];
for cnd = 1:length(settings.conditions)
    trials_info.trial_numbers_per_condition{cnd} = [];
    trials_info.stimuli{cnd} = [];
    trials_info.trial_times_per_condition{cnd} = [];
    trials_info.trial_times_button_press =[];
end

%%
for block = settings.blocks
    % Choose which conditions to compare
    trials_info_temp = [];
    settings.run_type_file = sprintf('new_mouse_recording_in_cheetah_clock_part%i.log', block);
    [trials_info_temp, settings] = get_condition_numbers(settings); 

    % Get time points for all tokens of each condition for the paradigm log
     [trials_info_temp, settings] = get_condition_times(trials_info_temp, settings);

    % collect current results from all blocks into a single struct ('trials_info')
      trials_info.category_position = [trials_info.category_position; trials_info_temp.category_position];
      if settings.generate_key_press_rasters
        trials_info.key_was_pressed_after.sentence = [trials_info.key_was_pressed_after.sentence, ...
                                            trials_info_temp.key_was_pressed_after.sentence];
        trials_info.trial_times_button_press = [trials_info.trial_times_button_press, ...
                                            trials_info_temp.trial_times_button_press];
        trials_info.behavioral.key_was_pressed_after_sentence{block} = union(trials_info_temp.key_was_pressed_after.sentence, trials_info_temp.key_was_pressed_after.sentence);
      end
      
      for cnd = 1:length(settings.conditions)
          trials_info.trial_numbers_per_condition{cnd} = [trials_info.trial_numbers_per_condition{cnd}; trials_info_temp.trial_numbers_per_condition{cnd}];
          trials_info.stimuli{cnd} = [trials_info.stimuli{cnd}; trials_info_temp.stimuli{cnd}];
          trials_info.trial_times_per_condition{cnd} = [trials_info.trial_times_per_condition{cnd}, trials_info_temp.trial_times_per_condition{cnd}];
      end
end
trials_info.behavioral = calc_behav_performance(trials_info.behavioral.key_was_pressed_after_sentence, settings);

end
