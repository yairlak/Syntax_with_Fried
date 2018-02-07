clear all; close all; clc
addpath('functions')
%%
% patients = {'D011', '466', '469', '472'};
params = [];

%%  ----- Generate HTMLs ------
patient = 'En_01';
file_name = sprintf('syntax_single_unit_rasters_key_press_%s', patient);

% open file
fileID = fopen(fullfile('..', '..', [file_name '.html']), 'w');

% Begining of file
fprintf(fileID, '<html>\n');
fprintf(fileID, '<head>\n');
fprintf(fileID, '<title>Raster plots</title>\n');
fprintf(fileID, '</head>\n');
fprintf(fileID, '<body>\n');

%%
% fprintf(fileID, '<font_size="14">Raster plots for all units. </font>\n');

for curr_cluster = 1:35
        title_str = sprintf('Cluster #%i (left - words, right - sentences)', curr_cluster);
        fprintf(fileID, '<font_size="14">%s </font>\n', title_str);
        fprintf(fileID, '<br>\n');
        
        % Words
        fig_name = sprintf('raster_button_press_patient=%s_unit_name=CSC%i_cluster_block_name=words_press.png', patient, curr_cluster);
        curr_filename = fullfile('Figures', 'Rasters', fig_name);
        fprintf(fileID, '<img class="right" src="%s" style="width:256px;height:256px;">\n', curr_filename);
        % Sentences
        fig_name = sprintf('raster_button_press_patient=%s_unit_name=CSC%i_cluster_block_name=sentences.png', patient, curr_cluster);
        curr_filename = fullfile('Figures', 'Rasters', fig_name);
        fprintf(fileID, '<img class="right" src="%s" style="width:256px;height:256px;">\n', curr_filename);
        fprintf(fileID, '<br>\n');
end

fclose(fileID);