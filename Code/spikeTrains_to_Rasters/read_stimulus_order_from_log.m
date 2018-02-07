clear all; close all; clc

%%
patients = {'En_02'};
block_names = {'sentences'};
settings.patient = patients{1};
settings.block_name = block_names{1};
[settings, ~] = load_settings_params(settings);

fid = fopen(fullfile(settings.path2data, settings.run_type_file), 'r');

trial = 1;
while ~feof(fid)
    curr_line = fgets(fid);
    curr_fields = strsplit(curr_line);
    if (strcmp(curr_fields{2}, 'DISPLAY_PICTURE') || strcmp(curr_fields{2}, 'DISPLAY_TEXT')) && ~strcmp(curr_fields{3}, 'OFF') 
%         trial_times{trial} = curr_fields{1};
%         trial_labels{trial} = curr_fields{3};
        sentence_numnber{trial} = curr_fields{4};
%         word_numnber_in_sentence{trial} = curr_fields{5};
%         word_string{trial} = curr_fields{6};
        trial = trial + 1;
    end
end

sentence_numnber = union(sentence_numnber, sentence_numnber, 'stable');