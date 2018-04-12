function [trials_info, settings] = get_condition_numbers(settings)
% Load code data

if ~isempty(settings.conditions)
    fid = fopen(fullfile(settings.path2data, settings.run_type_file), 'r');
    trial = 1;
    while ~feof(fid)
        curr_line = fgets(fid);
        curr_fields = strsplit(curr_line);
        if ((strcmp(curr_fields{2}, 'DISPLAY_PICTURE') || strcmp(curr_fields{2}, 'DISPLAY_TEXT')) && ~strcmp(curr_fields{3}, 'OFF'))
            IX_sentence_numnber{trial} = curr_fields{4};
            IX_wav = strfind(IX_sentence_numnber{trial}, '.wav');
            if ~isempty(IX_wav)
                IX_sentence_numnber{trial} = IX_sentence_numnber{trial}(1:IX_wav-1);
            end   
            trial = trial + 1;
        elseif strcmp(curr_fields{2}, 'AUDIO_PLAYBACK_ONSET') % Audio block
            wav_filename =  curr_fields{4};
            IX_wav = strfind(wav_filename, '.wav');
            num_file = wav_filename(1:IX_wav-1);
            IX_sentence_numnber{trial} = num_file; 
            trial = trial + 1;
        end
    end
    IX_sentence_numnber = union(IX_sentence_numnber, IX_sentence_numnber, 'stable');
    IX_sentence_numnber = cellfun(@str2num, IX_sentence_numnber)';
    [num, txt, ~] = xlsread(settings.feautre_codes_file, 1);
    IX_in_exp = num(2:end,1);
    IX_in_exp = IX_sentence_numnber(IX_in_exp);
    codes = num(2:end,4:end);
    txt = txt(3:end, :);
    trials_info.category_position = codes(:, 97:99);
    [~, perm_vec] = sort(IX_in_exp);
    trials_info.category_position = trials_info.category_position(perm_vec, :);
    % codes = codes(IX_in_exp, :);

%% set conditions
    cnt_feature_values = 0;
    for cnd = 1:length(settings.conditions)
        curr_columns = settings.conditions{cnd};
        curr_columns_pos = curr_columns(curr_columns>0)  - 3; % -3 because columns start at Column D in excel features file
        curr_columns_neg = -1*curr_columns(curr_columns<0) - 3;
        curr_IXs_pos = codes(:, curr_columns_pos);
        curr_IXs_neg = codes(:, curr_columns_neg);
        curr_IXs_neg(curr_IXs_neg<0) = 1;
        curr_IXs = [curr_IXs_pos ~curr_IXs_neg;];
        if ~isempty(find(curr_IXs>1)) % If not binary feature
                if size(curr_IXs, 2) == 1 % Only for a single column of non-binary features
                        feature_values = unique(curr_IXs);
                        for val = 1:length(feature_values)
                            cnt_feature_values = cnt_feature_values + 1;
                            curr_val = feature_values(val);
                            IX_curr_val = (curr_IXs == curr_val);
%                             curr_condition_trial_numbers = find(IX_curr_val);
%                             trial_numbers_per_condition{cnt_feature_values} = IX_in_exp(curr_condition_trial_numbers);
                            trials_info.trial_numbers_per_condition{cnt_feature_values} = IX_in_exp(IX_curr_val);
                            trials_info.stimuli{cnt_feature_values} =txt(IX_curr_val, 1);
                            settings.conditions_labels{cnt_feature_values} = sprintf('value__%i', curr_val);
                        end
                else
                    error('Condition #%i - more than a single column of a non-binary feature', cnd)
                end
        else % Intersect multi columns of binary features
%                 curr_IXs = curr_IXs > 0; % Remove -1 represnting irrelevant
                curr_IXs_pos = curr_IXs_pos > 0;
                curr_IXs = [curr_IXs_pos ~curr_IXs_neg;];
                if ~isempty(settings.conditions_union)
                    if settings.conditions_union(cnd)
                        IX_intersection = any(curr_IXs, 2);
                    else
                        IX_intersection = all(curr_IXs, 2);
                    end
                else % default is to instersect (and not to union) columns
                    IX_intersection = all(curr_IXs, 2);
                end
                trials_info.trial_numbers_per_condition{cnd} = IX_in_exp(IX_intersection);
                trials_info.stimuli{cnd} =txt(IX_intersection, 1);
                if size(settings.conditions_labels) ~= size(settings.conditions)
                       settings.conditions_labels{cnd} = ['Condition_' num2str(cnd)];    
                end
        end
    end
else
    trials_info.trial_numbers_per_condition = [];
    settings.conditions_labels = {'All__Trials'};
    trials_info.stimuli = [];
    
    % Syntactic category positions in sentence:
    [num, ~, ~] = xlsread(settings.feautre_codes_file, 1);
    IX_in_exp = num(2:end,1);
    codes = num(2:end,4:end);
    trials_info.category_position = codes(:, 97:99);
    [~, perm_vec] = sort(IX_in_exp);
    trials_info.category_position = trials_info.category_position(perm_vec, :);
end

    end