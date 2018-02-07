function custom_events = create_epochs_and_events(trials_info, settings)
% Returns:
% custom_events: num_events x 3

%% Generate the event list
custom_events = []; cnt = 1;
for cnd = 1:length(trials_info.trial_times_per_condition)
         curr_condition_trials_timings = trials_info.trial_times_per_condition{cnd};
         curr_condition_trials_timings = curr_condition_trials_timings/1e3; % from microsec to ms
         num_trials_of_curr_condition = length(curr_condition_trials_timings);
         st = cnt; ed = cnt + num_trials_of_curr_condition - 1;
         % !!!!!!! SUBTRACT settings.time0 (Added for macro units)
         custom_events(st:ed, 1) = curr_condition_trials_timings - settings.time0/1000;
         % !!!!!!!
         custom_events(st:ed, 3) = cnd-1;
         cnt = ed + 1;
end

end