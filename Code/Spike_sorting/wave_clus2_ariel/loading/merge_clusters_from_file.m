function [] = merge_clusters_from_file(ch, clus1, clus2)
% merge_clusters    

% Author: Ariel Tankus.
% Created: 01.02.2006.


min_clus = min(clus1, clus2);
max_clus = max(clus1, clus2);

if (min_clus < 0)
    error('clus1 and clus2 must be non-negative.');
end

filename = sprintf('times_CSC%d.mat', ch);
[success, message, messageid] = copyfile(filename, [filename, '.bkp']);
if (~success)
    fprintf('Failed to backup %s, merge cancelled:\n%s\nError code: %d', ...
            filename, message, messageid);
    return;
end

load(filename);
if (max_clus > max(cluster_class(:, 1)))
    error('max_clus (%d) outside range of cluster classes (%d).', max_clus, ...
          max(cluster_class(:, 1)));
end

max_clus_inds = find(cluster_class(:, 1) == max_clus);
cluster_class(max_clus_inds, 1) = min_clus;    % add max_clus to min_clus.

% redefine cluster numbers of clusters with higher number than max_clus,
% to maintain consecutive cluster numbers.
higher_than_clus_inds = find(cluster_class(:, 1) > max_clus);
if (~isempty(higher_than_clus_inds))
    cluster_class(higher_than_clus_inds, 1) = ...
        cluster_class(higher_than_clus_inds, 1) - 1;
end
if (exist('comments', 'var'))
    comments = comments([1:(max_clus-1), (max_clus+1):end]);
    save(filename, 'cluster_class', 'inspk', 'par', 'spikes', 'comments');
else
    save(filename, 'cluster_class', 'inspk', 'par', 'spikes');
end
