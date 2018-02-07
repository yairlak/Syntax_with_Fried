function [trial_numbers_per_condition, conditions_labels] = get_condition_numbers(settings);
% Load code data
xls_file = fullfile('..','..','Paradigm', 'CODES sentences 220117.xlsx');
[num, txt, ~] = xlsread(xls_file, 1);
IX_in_exp = num(:,1);
codes = num(:,4:end);
% codes = codes(IX_in_exp, :);

%% set conditions
for cnd = 1:length(settings.conditions)
    curr_columns = settings.conditions{cnd};
    curr_IXs = codes(:, curr_columns);
    IX_intersection = all(curr_IXs, 2);
    curr_condition_trial_numbers = find(IX_intersection);
    trial_numbers_per_condition{cnd} = IX_in_exp(curr_condition_trial_numbers);
    if size(settings.conditions_labels) == size(settings.conditions)
        conditions_labels{cnd} = settings.conditions_labels{cnd};    
    else
        conditions_labels{cnd} = ['Condition_' num2str(cnd)];    
    end

end

end