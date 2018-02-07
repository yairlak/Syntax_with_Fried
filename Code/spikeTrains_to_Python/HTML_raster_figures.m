clear all; close all; clc
addpath('functions')
%%
% patients = {'D011', '466', '469', '472'};
params = [];

%%  ----- Generate HTMLs ------
file_name = sprintf('main_rasters_syntax_single_unit');

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

files = dir(fullfile('..', '..', 'Figures', '*.png'));
for f = 1:length(files)
        fig_name = files(f).name;
        curr_filename = fullfile('Figures', fig_name);
        first_name = fig_name(1:end-4);
        
%         fprintf(fileID, '<div class="section_title"><u> <font size="6"> %s</font></u></div>\n', settings.unit_name);
        
%         settings_fields = {'unit_name', 'patient'};
%         params_fields = [];
%         curr_filename = get_file_name_curr_run(settings, params, settings_fields, params_fields);
%         curr_filename = [curr_filename '.png'];
        
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<font_size="14">%s </font>\n', first_name);
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<img class="right" src="%s" style="width:1024px;height:512px;">\n', curr_filename);
        fprintf(fileID, '<br>\n');
%         fprintf(fileID, '<figcaption>%s</figcaption>', settings.unit_name);
        
%     end
end

fclose(fileID);