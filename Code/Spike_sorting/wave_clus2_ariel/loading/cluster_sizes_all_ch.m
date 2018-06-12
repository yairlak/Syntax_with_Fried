function [] = cluster_sizes_all_ch()
% cluster_sizes    

% Author: Ariel Tankus.
% Created: 20.06.2006.


file_names = ls_to_cell('times_CSC*.mat');

for i=1:length(file_names)
    load(file_names{i});
    cur_ch = sscanf(file_names{i}(10:end), '%d');
    for j=1:length(unique(cluster_class(:, 1)))
        fprintf('Ch: %d, Cl: %d, #spikes = %d\n', cur_ch, j-1, ...
                sum(cluster_class(:, 1) == j-1));
    end
end
