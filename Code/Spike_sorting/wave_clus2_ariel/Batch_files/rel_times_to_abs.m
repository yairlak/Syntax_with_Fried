function rel_times_to_abs(ch_list)
% rel_times_to_abs    

% Author: Ariel Tankus.
% Created: 14.09.2009.


bkp_subdir = './rel_times_files';

if (~exist(bkp_subdir, 'dir'))
    mkdir(bkp_subdir);
else
    error(sprintf(['Bkp file already exists.  This function should not be' ...
                   ' run\nsuccessively in the same directory, to protect' ...
                   ' original\n(relative) times files.\n']));
end
[success, message, messageid] = copyfile('./times_CSC*.mat', bkp_subdir);
if (~success)
    error('Cannot back times files up into %s .', bkp_subdir);
end

fprintf('    Ch:');
for i=1:length(ch_list)

    fprintf(' %d', ch_list(i));

    first_time_stamp = read_first_time_stamp(sprintf('CSC%d.Ncs', ch_list(i)));
    offset_ms = first_time_stamp ./ 1000;
    
    times_file = sprintf('./times_CSC%d.mat', ch_list(i));
    if (~exist(times_file, 'file'))
        continue;
    end
    load(times_file);
    
    cluster_class(:, 2) = cluster_class(:, 2) + offset_ms;
    
    if (exist('comments', 'var'))
        save(times_file, 'cluster_class', 'comments', 'inspk', 'par', 'spikes');
    else
        save(times_file, 'cluster_class', 'inspk', 'par', 'spikes');
    end
    
    clear cluster_class comments inspk par spikes;

end
fprintf('\n');
