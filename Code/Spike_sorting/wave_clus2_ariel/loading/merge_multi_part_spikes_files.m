function [] = merge_multi_part_spikes_files(dir_list, target_dir)
% merge_multi_part_spikes_files    

% Author: Ariel Tankus.
% Created: 26.03.2008.


num_ch = 64;

cur_wd = pwd;

num_parts = length(dir_list);
index_cell  = cell(num_parts, 1);
spikes_cell = cell(num_parts, 1);

for ch=1:num_ch

    fprintf('Ch: %d\n', ch);

    % Accumulate all spikes of the same channel from all parts:
    for i=1:num_parts
        cd(cur_wd);              % just in case dir_list{i} is relative.
        cd(dir_list{i});
        load(sprintf('CSC%d_spikes.mat', ch));
        index_cell{i}  = index;
        spikes_cell{i} = spikes;
    end
    
    [index, spikes, part_id] = multi_part_spikes(index_cell, spikes_cell);
    cd(cur_wd);              % just in case target_dir is relative.
    cd(target_dir);
    save(sprintf('CSC%d_spikes.mat', ch), 'index', 'spikes', 'part_id', ...
         'dir_list', 'target_dir');
    
end

cd(cur_wd);
