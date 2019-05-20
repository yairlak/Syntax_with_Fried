function [classes, comments] = merge_clusters(cluster_ids, classes, comments)
% merge_clusters    Merge two clusters. 

% Author: Ariel Tankus.
% Created: 13.06.2006.


min_clus = min(cluster_ids);
num_clusters = length(cluster_ids);

if (min_clus < 0)
    error('cluster_ids must be non-negative.');
end

if (max(cluster_ids) > max(classes))
    error('max_clus (%d) outside range of cluster classes (%d).', ...
          max(cluster_ids), max(classes));
end

for i=2:num_clusters
    cur_clus_inds = find(classes == cluster_ids(i));
    if (~isempty(cur_clus_inds))
        classes(cur_clus_inds) = min_clus;    % add cur cluster to
                                                       % min_clus.
    end
end

% squeeze cluster numbers, to maintain consecutive range of cluter IDs:
sorted_cluster_ids = sort(cluster_ids);
for i=2:(num_clusters - 1)
    cur_clus_inds = find((classes > sorted_cluster_ids(i)) & ...
                         (classes < sorted_cluster_ids(i+1)));
    if (~isempty(cur_clus_inds))
        classes(cur_clus_inds) = classes(cur_clus_inds)-i+1;
    end
end
cur_clus_inds = find((classes > sorted_cluster_ids(end)));
if (~isempty(cur_clus_inds))
    classes(cur_clus_inds) = classes(cur_clus_inds)-num_clusters+1;
end

if (nargin >= 4)
    comments = comments(setdiff(1:num_clusters, sorted_cluster_ids));
end
