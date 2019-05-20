function [] = channel_sizes()
% channel_sizes    

% Author: Ariel Tankus.
% Created: 20.06.2006.


file_names = ls_to_cell('times_CSC*.mat');

for i=1:length(file_names)
    load(file_names{i});
    cur_ch = sscanf(file_names{i}(10:end), '%d');
    fprintf('Ch: %d, #spikes = %d\n', cur_ch, size(cluster_class, 1));
end
