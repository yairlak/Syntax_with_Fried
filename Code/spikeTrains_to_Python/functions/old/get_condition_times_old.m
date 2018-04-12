function trial_times_per_condition = get_condition_times(trial_numbers_per_condition, settings);

%% read paradigm logs
fid = fopen(fullfile(settings.path2data, settings.run_type_file), 'r');
all_trials =textscan(fid, '%s %s');
fclose(fid);
trial_times = all_trials{1};
trial_labels = all_trials{2};
% Omit prefix, e.g., 'word', 'nonword', and keep only serial number
trial_labels = cellfun(@(x) x((strfind(x, '_')+1):end), trial_labels, 'UniformOutput', false);

%% get trial timing for each condition
for cnd = 1:length(trial_numbers_per_condition)
    curr_condition = trial_numbers_per_condition{cnd};
    trial_times_of_curr_condition = [];
    for token = 1:length(curr_condition)
        curr_token_number = curr_condition(token);
        curr_token_number = 2*curr_token_number - 1; % First word (1-180 to 1-360)
        IX = strcmp(num2str(curr_token_number), trial_labels);
        if sum(IX)~=1
            error('No match between token numbers and paradigm log file')
        else
            trial_times_of_curr_condition(token) = str2double(trial_times{IX});
        end
    end
    % Add found trial timings to output cell array
    trial_times_per_condition{cnd} = trial_times_of_curr_condition;
end

end