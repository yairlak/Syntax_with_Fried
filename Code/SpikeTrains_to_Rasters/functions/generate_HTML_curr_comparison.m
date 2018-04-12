function generate_HTML_curr_comparison(trials_info, figure_names, settings)

% open file
file_name = sprintf('rasters_syntax_%s_%s_%s_%s.html', settings.patient, settings.block_name, settings.comparison_name, settings.lock_to_word);
fileID = fopen(fullfile('..', '..', file_name), 'w');

% Begining of file
fprintf(fileID, '<html>\n');
fprintf(fileID, '<head>\n');
fprintf(fileID, '<title>Raster plots</title>\n');
fprintf(fileID, '</head>\n');
fprintf(fileID, '<body>\n');

% Explanation
fprintf(fileID, '<br>\n');
fprintf(fileID, '<font_size="14">%s </font>\n', settings.comparison_comments);
fprintf(fileID, '<br>\n');
fprintf(fileID, '<font_size="14"> See all sentences from each condition at the bottom of the page.</font>\n');
fprintf(fileID, '<br>\n');
fprintf(fileID, '<br>\n');

% ERPs
curr_fig_name = sprintf('ERP0_%s_%s_%s_%s.png', settings.patient, settings.block_name, settings.comparison_name, settings.lock_to_word);
curr_fig_name = fullfile('Figures', 'figures_ERP', curr_fig_name);
fprintf(fileID, '<img class="right" src="%s" style="width:1024px;height:512px;">\n', curr_fig_name);
fprintf(fileID, '<br>\n');
curr_fig_name = sprintf('ERP1_%s_%s_%s_%s.png', settings.patient, settings.block_name, settings.comparison_name, settings.lock_to_word);
curr_fig_name = fullfile('Figures', 'figures_ERP', curr_fig_name);
fprintf(fileID, '<img class="right" src="%s" style="width:1024px;height:512x;">\n', curr_fig_name);
fprintf(fileID, '<br>\n');

% GAT
curr_fig_name = sprintf('gat_%s_%s_%s_%s.png', settings.patient, settings.block_name, settings.comparison_name, settings.lock_to_word);
curr_fig_name = fullfile('Figures', 'figures_GAT', curr_fig_name);
fprintf(fileID, '<img class="right" src="%s" style="width:512px;height:256px;">\n', curr_fig_name);
curr_fig_name = sprintf('gat_diag_%s_%s_%s_%s.png', settings.patient, settings.block_name, settings.comparison_name, settings.lock_to_word);
curr_fig_name = fullfile('Figures', 'figures_GAT', curr_fig_name);
fprintf(fileID, '<img class="right" src="%s" style="width:512px;height:256px;">\n', curr_fig_name);
fprintf(fileID, '<br>\n');

for unit = 1:size(figure_names, 1)
    curr_fig_name = figure_names{unit, 1};
    cluster = get_cluster_info(curr_fig_name, settings);
    fprintf(fileID, '<font_size="14">%s </font>\n', ['Location ' cluster.name ' cluster #' num2str(cluster.number) '  mean ' cluster.firing_rate]);
    fprintf(fileID, '<br>\n');
    for cnd = 1:size(figure_names, 2)         
           curr_fig_name = figure_names{unit, cnd};
           curr_fig_name = fullfile('Figures', 'Rasters', curr_fig_name);
           fprintf(fileID, '<img class="right" src="%s" style="width:256px;height:256px;">\n', curr_fig_name);
    end
    fprintf(fileID, '<br>\n');
end

% Stimuli info
fprintf(fileID, '<pre>');
fprintf(fileID, '<font_size="12">[Num] \t\t [Stimulus] \t\t [Time in block (ms)] </font><br>\n');
for cnd = 1:length(trials_info.stimuli)
    fprintf(fileID, '<font_size="12">Condition %s </font><br>\n', settings.conditions_labels{cnd});
    curr_stimuli = trials_info.stimuli{cnd};
    curr_IXs = trials_info.trial_numbers_per_condition{cnd};
    curr_times = trials_info.trial_times_per_condition{cnd}/1000;
    for trl = 1:length(curr_stimuli)
        fprintf(fileID, '<font_size="12">%i \t\t %s \t\t %f </font><br>\n', curr_IXs(trl), curr_stimuli{trl}, curr_times(trl));
    end
    fprintf(fileID, '<br>\n');
end
fprintf(fileID, '</pre>');
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
switch settings.patient
    case 'ArM01'
        clusters_info = importdata(fullfile(settings.path2data, 'firing_rates_report.txt'));
        clusters_info = clusters_info(6:end, :);
        curr_cluster_info = clusters_info{cluster.number, :};
        cluster.name = curr_cluster_info(20:24);
        cluster.firing_rate = curr_cluster_info(28:49);
        % cluster.single_or_multi = curr_cluster_info(53:end);
    case 'En_01'
        script_location = fullfile('..', '..', 'Data', 'Patients', settings.patient, settings.block_name, 'clusters_electrode_montage.m');
        copyfile(script_location, pwd)
        m = clusters_electrode_montage;
        delete('clusters_electrode_montage.m')
        % Extract info
        cluster_number = cell(size(m, 1), 1);
        cluster_number(:) = {cluster.number};
        IX = cellfun(@ismember, cluster_number, m(:, 1));
        cluster.name = m{IX, 2};
        cluster.firing_rate = [];
end
end
