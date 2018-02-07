clear all; close all; clc
addpath('functions')

%%  raster HTML per block
patient = 'En_01';
block_name = 'words';
comparison_name1 = 'Num_of_Morphemes';
comparison_name = 'Num+Of+Morphemes';
clusters = 1:35;

clusters = [11:12, 22:24, 29:33];
values = 0:4;

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
        fprintf(fileID, '<font_size="14">Cluster %i </font>\n', cluster);
        fprintf(fileID, '<br>\n');
                
        for val = 1:length(values)
            curr_val = values(val);
            fig_name = sprintf('raster_patient=%s_unit_name=CSC%i_cluster_comparison_name=%s_value__%i_block_name=%s', patient, cluster, comparison_name, curr_val, block_name);
            if strcmp(block_name, 'sentences')
                fig_name = [fig_name '_lock_to_word=first'];
            end
            fig_name = [fig_name '.png'];
            curr_filename = fullfile('Figures', 'Rasters', fig_name);
            fprintf(fileID, '<img class="right" src="%s" style="width:256px;height:256px;">\n', curr_filename);
        end
        fprintf(fileID, '<br>\n');
        
end

fclose(fileID);