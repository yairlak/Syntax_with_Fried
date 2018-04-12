function generate_HTML_comparison(figure_names, file_name, settings)

% open file
fileID = fopen(fullfile('..', '..', [file_name '.html']), 'w');

% Begining of file
fprintf(fileID, '<html>\n');
fprintf(fileID, '<head>\n');
fprintf(fileID, '<title>Raster plots</title>\n');
fprintf(fileID, '</head>\n');
fprintf(fileID, '<body>\n');

for fig = 1:length(figure_names)
        curr_fig_name = figure_names{fig};
        curr_fig_name = fullfile('Figures', curr_fig_name);
        cluster = get_cluster_info(curr_fig_name, settings);
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<font_size="14">%s </font>\n', ['Location ' cluster.name ' cluster #' num2str(cluster.number) '  mean ' cluster.firing_rate]);
        fprintf(fileID, '<br>\n');
        fprintf(fileID, '<img class="right" src="%s" style="width:1024px;height:512px;">\n', curr_fig_name);
        fprintf(fileID, '<br>\n');
end

fclose(fileID);

end

function cluster = get_cluster_info(file_name, settings)
% Extract cluster number from file name
st = strfind(file_name, 'CSC');
file_name = file_name(st:end);
ed = strfind(file_name, '_');
ed = ed(1)-1;
cluster.number= str2double(file_name(4:ed));

% Load cluster info and montage
clusters_info = importdata(fullfile(settings.path2data, 'firing_rates_report.txt'));
clusters_info = clusters_info(6:end, :);
curr_cluster_info = clusters_info{cluster.number, :};
cluster.name = curr_cluster_info(20:24);
cluster.firing_rate = curr_cluster_info(28:49);
% cluster.single_or_multi = curr_cluster_info(53:end);
end
