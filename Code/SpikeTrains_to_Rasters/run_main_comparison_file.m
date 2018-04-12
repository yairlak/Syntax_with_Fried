clear all; close all; clc
addpath('functions')
warning('off')

%%
patients = {'En_01'};
% block_names = {'words', 'words_press', 'nonwords', 'nonwords_press', 'sentences'};
block_names = {'sentences'};
comparison_list = [7];%,10,12,18]; % Comparions number from file - which comparisons in file to run. If empty, then run all.

%%
generate_rasters_and_corresponding_HTMLs = true;
generate_HTML_curr_block = true;

%%
if generate_rasters_and_corresponding_HTMLs
    for p = 1:length(patients)
        for bn = 1:length(block_names)
            settings.patient = patients{p};
            settings.block_name = block_names{bn};
            file_name = sprintf('Comparisons %s %s.xlsx', patients{p}, block_names{bn});
            [~, comparison_file, ~] = xlsread(fullfile('..', '..', 'Paradigm', file_name));
            if isempty(comparison_list)
                comparison_list = 1:size(comparison_file, 1)-1;
            end
            for comp = (comparison_list+1)
                    % Comparison Info:
                    settings.conditions = eval(comparison_file{comp, 2});
                    settings.comparison_name = comparison_file{comp, 1};
                    if ~isempty(comparison_file{comp, 3})
                        settings.conditions_labels = eval(comparison_file{comp, 3});
                    end
                    settings.lock_to_word = comparison_file{comp, 4};
                    settings.comparison_comments = comparison_file{comp, 5};
                    fprintf('PATIENT %s, BLOCK %s, COMPARISON %s\n', patients{p}, block_names{bn}, settings.comparison_name);
                    % Generate rasters:
                    main_spike_trains_to_rasters                
                    % Collect rasters to HTML:
                    generate_HTML_curr_comparison(trials_info, figure_names, settings);
            end
            clearvars 'settings' 'trials_info' 'rasters' 'figure_names'
        end
    end
end

fclose('all')
%% HTML for current block
if generate_HTML_curr_block
    %  Generate HTML
    file_name = sprintf('rasters_syntax_%s_%s', patients{1}, block_names{1});
    fileID = fopen(fullfile('..', '..', [file_name '.html']), 'w');

    % Begining of file
    fprintf(fileID, '<html>\n');
    fprintf(fileID, '<head>\n');
    fprintf(fileID, '<title>Rasters - %s %s</title>\n', patients{1}, block_names{1});
    fprintf(fileID, '</head>\n');
    fprintf(fileID, '<body>\n');
    
    fprintf(fileID, '<font>Patient %s %s</font><br><br>\n', patients{1}, block_names{1});
    fprintf(fileID, '<a href="rasters_syntax_%s_%s_all_trials_last.html" title="all_trials"> All trials</a><br><br>', patients{1}, block_names{1});
    
    file_name = sprintf('Comparisons %s %s.xlsx', patients{1}, block_names{1});
    [~, comparison_file, ~] = xlsread(fullfile('..', '..', 'Paradigm', file_name));
    if isempty(comparison_list)
        comparison_list = 1:size(comparison_file, 1)-1;
    end            
    for comp = (comparison_list+1)
                % Comparison Info:
                comparison_name = comparison_file{comp, 1};
                lock_to_word = comparison_file{comp, 4};
                fprintf(fileID, '<a href="rasters_syntax_%s_%s_%s_%s.html" title="%s"> %s</a><br><br>\n', patients{1}, block_names{1}, comparison_name, lock_to_word, comparison_name, comparison_name);
                % Generate rasters:
    end
end

fclose(fileID);