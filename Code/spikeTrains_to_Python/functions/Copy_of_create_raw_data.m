function [custom_raw, custom_raw_smoothed, unit_names] = create_raw_data(settings)
% Returns:
% custom_raw: num_channels x num_timepoints

%% Generate for the raw object the corresponding mat from spike trains
all_units = dir(fullfile(settings.path2data, 'CSC*.mat'));
for unit = 1:length(all_units)
    curr_file_name = all_units(unit).name;
    curr_data = load(fullfile(settings.path2data, curr_file_name));
    cluster = get_cluster_info(curr_file_name, settings);
    unit_names{unit} = cluster.name;
    custom_raw(unit, round(curr_data.spike_times_sec * 1000)) = 1;%sec to ms
end

%% Smooth custom raw
for unit = 1:size(custom_raw, 1)
    curr_time_series = custom_raw(unit, :);
    N = 1000; % num samples in gaussian window
    gaussian_width = 50; % in samples (ms)
    alpha = (N-1)/(2*gaussian_width);
    gaussian_window = gausswin(1000, alpha);
    smoothed_time_series = filter(gaussian_window, 1, curr_time_series);
    smoothed_time_series(1:round(N/2)) = [];
    smoothed_time_series(end:end+length(1:round(N/2))) = 0;
    custom_raw_smoothed(unit, :) = smoothed_time_series;
end

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

% function cluster = get_cluster_info(file_name, settings)
% % Extract cluster number from file name
% st = strfind(file_name, 'CSC');
% file_name = file_name(st:end);
% ed = strfind(file_name, '_');
% ed = ed(1)-1;
% cluster.number= str2double(file_name(4:ed));
% 
% % Load Ariel's cluster info and montage
% clusters_info = importdata(fullfile(settings.path2data, 'firing_rates_report.txt'));
% clusters_info = clusters_info(6:end, :);
% curr_cluster_info = clusters_info{cluster.number, :};
% cluster.name = curr_cluster_info(20:24);
% cluster.firing_rate = curr_cluster_info(28:49);
% % cluster.single_or_multi = curr_cluster_info(53:end);
% end
