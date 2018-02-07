clear all; close all; clc
addpath('functions')
warning('off')
%%
hospital = 'UCLA';
settings.hospital = 'UCLA';
settings.blocks = [1:2]; % For example, with En_02 there were 6 blocks: visual #1,3,5 and auditory 2,4,6.
blocks_str = num2str(settings.blocks);
blocks_str = strrep(blocks_str,' ','');
settings.blocks_str = blocks_str;
patients = {'patient_479'};
run_names = {'sentences'}; % 'words', 'words_press', 'nonwords', 'nonwords_press', 'sentences'
settings.block_type = 'mixed'; %e.g., 'visual', 'audio', 'mixed'
comparison_list = [1:6];%,10,12,18]; % Comparions number from file - which comparisons in file to run. If empty, then run all.

%%
run_PCA = false;
generate_rasters = true;
generate_HTML_all_comparisons = false;

%%
for p = 1:length(patients)
%     for bn = 1:length(block_names)
        settings.patient = patients{p};
        settings.run_name = run_names{1};
        file_name = sprintf('Comparisons %s %s %s.xlsx', settings.hospital, patients{p}, run_names{1});
        [~, comparison_file, ~] = xlsread(fullfile('..', '..', 'Paradigm', file_name));
        if isempty(comparison_list)
            comparison_list = 1:size(comparison_file, 1)-1;
        end
        for comp = (comparison_list+1)
                % Comparison Info:
                settings.conditions = eval(comparison_file{comp, 2});
                if ~isempty(comparison_file{comp, 6})
                    settings.conditions_union = eval(comparison_file{comp, 6});
                    if length(settings.conditions) ~= length(settings.conditions_union)
                        error('Check Excel comparison files. Make sure Column C and G have the same length')
                    end
                else
                    settings.conditions_union = [];
                end
                settings.comparison_name = comparison_file{comp, 1};
                if ~isempty(comparison_file{comp, 3})
                    settings.conditions_labels = eval(comparison_file{comp, 3});
                end
                settings.lock_to_word = comparison_file{comp, 4};
                settings.comparison_comments = comparison_file{comp, 5};
                fprintf('HOSPITAL %s, PATIENT %s, BLOCKS %s, COMPARISON %s\n', settings.hospital, patients{p}, blocks_str, settings.comparison_name);
                % Generate rasters:
                main_spike_trains_to_rasters                
                % Collect rasters to HTML:
                generate_HTML_curr_comparison(trials_info, figure_names, settings);
        end
        clearvars 'settings' 'trials_info' 'rasters' 'figure_names'
%     end
end

fclose('all')
%% HTML for current block
if generate_HTML_all_comparisons
    settings.hospital = 'UCLA';
    settings.patient = patients{1};
    settings.run_name = run_names{1};
    [settings, ~] = load_settings_params(settings);
    settings.block_type = 'mixed';
    %  Generate HTML
    file_name = sprintf('rasters_syntax_%s_%s', patients{1}, run_names{1});
    fileID = fopen(fullfile('..', '..', [file_name '.html']), 'w');

    % Begining of file
    fprintf(fileID, '<html>\n');
    fprintf(fileID, '<head>\n');
    fprintf(fileID, '<title>Rasters - %s %s</title>\n', patients{1}, run_names{1});
    fprintf(fileID, '</head>\n');
    fprintf(fileID, '<body>\n');

    fprintf(fileID, '<font>Patient %s %s</font><br><br>\n', patients{1}, run_names{1});
    fprintf(fileID, '<a href="rasters_syntax_%s_%s_all_trials_last.html" title="all_trials"> All trials</a><br><br>', patients{1}, run_names{1});

    file_name = sprintf('Comparisons %s %s %s.xlsx', hospital, patients{p}, run_names{1});
    [~, comparison_file, ~] = xlsread(fullfile('..', '..', 'Paradigm', file_name));
    if isempty(comparison_list)
        comparison_list = 1:size(comparison_file, 1)-1;
    end            
    for comp = (comparison_list+1)
        % Comparison Info:
        comparison_name = comparison_file{comp, 1};
        lock_to_word = comparison_file{comp, 4};
        fprintf(fileID, '<a href="rasters_syntax_%s_%s_%s_%s_%s_%i.html" title="%s"> %s</a><br><br>\n', patients{1}, run_names{1}, comparison_name, lock_to_word, settings.block_type, settings.sort_sentences_according_length, comparison_name, comparison_name);
        % Generate rasters:
    end
fclose(fileID);    
end
