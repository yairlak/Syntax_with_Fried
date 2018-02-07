clear all; close all; clc
addpath('functions')

%%  raster HTML per block
% patient = 'En_01';
% block_name = 'sentences';
% comparison_name1 = 'all_trials';
% comparison_name = 'All+trials';
clusters = 1:35;

% Generate HTML file
file_name = sprintf('rasters_syntax_%s_%s_%s', patient, block_name, comparison_name1);
fileID = fopen(fullfile('..', '..', [file_name '.html']), 'w');

% Begining of file
fprintf(fileID, '<html>\n');
fprintf(fileID, '<head>\n');
fprintf(fileID, '<title>Raster plots</title>\n');
fprintf(fileID, '</head>\n');
fprintf(fileID, '<body>\n');

%%
for cluster = clusters
        
%         if ~strcmp(block_name, 'nonwords')
            fig_name = sprintf('raster_patient=%s_unit_name=CSC%i_cluster_comparison_name=%s_block_name=%s', patient, cluster, comparison_name, block_name);
%         else
%             fig_name = sprintf('raster_patient=%s_unit_name=CSC%i_cluster_comparison_name=%s_block_name=non_words', patient, cluster, comparison_name);
%         end
        if strcmp(block_name, 'sentences')
            fig_name = [fig_name '_lock_to_word=first'];
        end
        fig_name = [fig_name '.png'];
        curr_filename = fullfile('Figures', 'Rasters', fig_name);
                
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<font_size="14">Cluster %i </font>\n', cluster);
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<img class="right" src="%s" style="width:1024px;height:512px;">\n', curr_filename);
        fprintf(fileID, '<br>\n');

end

fclose(fileID);