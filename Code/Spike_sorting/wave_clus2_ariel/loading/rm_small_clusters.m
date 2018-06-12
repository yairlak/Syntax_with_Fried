function new_classes = rm_small_clusters(classes, min_clus)
% rm_small_clusters    

% Author: Ariel Tankus.
% Created: 05.09.2008.


new_classes = classes;
cluster_ids = unique(setdiff(classes, 0));
num_clusters = length(cluster_ids);

for i=1:num_clusters
    cl_inds = find(classes == cluster_ids(i));
    if (length(cl_inds) < min_clus)
        % cluster too small, move to trash:
        new_classes(cl_inds) = 0;
    end
end
