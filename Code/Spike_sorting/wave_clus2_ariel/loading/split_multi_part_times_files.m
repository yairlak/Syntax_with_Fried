function [] = split_multi_part_times_files(src_dir)
% split_multi_part_times_files    

% Author: Ariel Tankus.
% Created: 27.03.2008.


num_ch = 64;

cur_wd = pwd;

index_cell  = cell(num_parts, 1);
spikes_cell = cell(num_parts, 1);

for ch=1:num_ch

    fprintf('Ch: %d\n', ch);
    cd(cur_wd);
    cd(src_dir);
    load(sprintf('CSC%d_spikes.mat', ch));
    load(sprintf('times_CSC%d.mat', ch));
    
    multi_inspk = inspk;
    multi_spikes = spikes;
    multi_cluster_class = cluster_class;
    
    num_parts = length(dir_list);
    % Accumulate all spikes of the same channel from all parts:
    for i=1:num_parts
        cd(cur_wd);              % just in case dir_list{i} is relative.
        cd(dir_list{i});
        
        inds = find(part_id == i);
        spikes        = multi_spikes(inds, :);
        inspk         = multi_inspk(inds, :);
        cluster_class = multi_cluster_class(inds, :);

        save(sprintf('times_CSC%d.mat', ch), 'spikes', 'inspk', ...
             'cluster_class', 'par', 'dir_list', 'target_dir');
    end
    
end

cd(cur_wd);
