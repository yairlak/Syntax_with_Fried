function [spike_data_all_units, unit_names] = load_spike_data(settings)
%% Read Ariel's spike-time files
all_units = dir(fullfile(settings.path2data, 'CSC*.mat'));
num_units = length(all_units);

%% For each unit, extract spike times and name
unit_names = cell(num_units, 2);%init array
spike_data_all_units = cell(1, num_units); %init array
for unit = 1:length(all_units) 
    curr_file_name = all_units(unit).name;
    curr_data = load(fullfile(settings.path2data, curr_file_name));
    curr_spike_train = curr_data.spike_times_sec * 1000; %sec to ms
    unit_names{unit, 1} = curr_file_name(1:end-4); %Cluster number
    spike_data_all_units{unit} = curr_spike_train; % Add to cell array
    
    cluster = get_cluster_info(curr_file_name, settings);
    unit_names{unit, 2} = cluster.name; %Cluster/unit name from electrode montage
end
    
end

function cluster = get_cluster_info(file_name, settings)
% Extract cluster number from file name
st = strfind(file_name, 'CSC');
file_name = file_name(st:end);
ed = strfind(file_name, '_');
ed = ed(1)-1;
cluster.number= str2double(file_name(4:ed));

% Load Ariel's cluster info and montage
clusters_info = importdata(fullfile(settings.path2data, 'firing_rates_report.txt'));
clusters_info = clusters_info(6:end, :);
curr_cluster_info = clusters_info{cluster.number, :};
cluster.name = curr_cluster_info(20:24);
cluster.firing_rate = curr_cluster_info(28:49);
% cluster.single_or_multi = curr_cluster_info(53:end);
end
