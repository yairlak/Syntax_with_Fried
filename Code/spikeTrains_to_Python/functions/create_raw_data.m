function [custom_raw, custom_raw_smoothed, unit_names, settings] = create_raw_data(settings)
% Returns:
% custom_raw: num_channels x num_timepoints

%% Generate for the raw object the corresponding mat from spike trains
all_units = dir(fullfile(settings.path2data, 'CSC*.mat'));
file_names = {all_units(:).name};
file_nums = cellfun(@(x) x(4:strfind(x,'_')-1), file_names, 'uniformoutput', false);
[file_nums_sorted, IX] = sort(str2double(file_nums));
all_units = all_units(IX);
for unit = 1:length(all_units)
    curr_file_name = all_units(unit).name;
    curr_data = load(fullfile(settings.path2data, curr_file_name));
    cluster = get_cluster_info(curr_file_name, settings);
    unit_names{unit} = cluster.name;
    custom_raw(unit, round((curr_data.spike_times_sec -curr_data.time0/1e6)* 1000)) = 1;%sec to ms
    if unit>1 % Sanity check
        if time0_previous ~= curr_data.time0
            error('Not all units have the same start time in current block')
        end
    end
    time0_previous = curr_data.time0;
    settings.time0 = curr_data.time0; % Save the last start time of block (assuming the same for all units)
end

%% Smooth custom raw
for unit = 1:size(custom_raw, 1)
    curr_time_series = custom_raw(unit, :);
    N = 1000; % num samples in gaussian window
    gaussian_width = 50; % in samples (ms)
    norm_factor = sqrt(2*pi*(gaussian_width*1e-3)^2);
    alpha = (N-1)/(2*gaussian_width);
    gaussian_window = gausswin(1000, alpha);
    smoothed_time_series = filter(gaussian_window, 1, curr_time_series);
    smoothed_time_series(1:round(N/2)) = [];
    smoothed_time_series(end:end+length(1:round(N/2))) = 0;
    fprintf('Smoothing unit %s %s\n', all_units(unit).name, unit_names{unit});
    custom_raw_smoothed(unit, :) = smoothed_time_series/norm_factor;
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
<<<<<<< HEAD
    case {'En_01', 'En_02', 'patient_479'}
        %script_location = fullfile('..', '..', 'Data', 'Patients', settings.patient, settings.block_name, 'clusters_electrode_montage.m');
        %copyfile(script_location, pwd)
        m = clusters_electrode_montage;
        %delete('clusters_electrode_montage.m')
=======
    case 'En_01'
        script_location = fullfile('..', '..', 'Data', 'Patients', settings.patient, settings.block_name, 'clusters_electrode_montage.m');
        copyfile(script_location, pwd)
        m = clusters_electrode_montage;
        delete('clusters_electrode_montage.m')
>>>>>>> 5b9b039709819b6943ba2d6fe6a2cb30b8113304
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
