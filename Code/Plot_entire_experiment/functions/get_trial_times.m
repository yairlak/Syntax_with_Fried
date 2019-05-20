function [times, labels] = get_trial_times(settings)
%% Load Ariel's file for stimulus onsets
fid = fopen(fullfile(settings.path2data, settings.run_type_file), 'r');
all_trials =textscan(fid, '%d %s');
fclose(fid);

%% Take odd 
labels = all_trials{2};
% find lables with 'pair' in it and 
trial_labels = cellfun(@(x) ~isempty(strfind(x, 'pair')), labels, 'UniformOutput', false);
IX = find(cell2mat(trial_labels));
% Take odd numbers - first word in the sentence
IX = IX(1:2:end); 
% Extract the corresponding times for the first-word labels
times = all_trials{1};
times = times(IX)/1000; %from usec to msec
labels = labels(IX);
end