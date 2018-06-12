function times_CSC = swap_cluster_ids(times_CSC, id1, id2)
% swap_cluster_ids    Swap the cluster IDs of two clusters.
%
%                     times_CSC = swap_cluster_ids(times_CSC, id1, id2)
%                     id1, id2 - 1x1 - cluster IDs to swap.
%                     times_CSC - struct (see load_times_CSC for fields) -
%
%                     See also:  load_times_CSC, load_save_time_CSC.

% Author: Ariel Tankus.
% Created: 27.01.2010.


cluster_ids = unique(times_CSC.cluster_class(:, 1));
if (~all(ismember([id1, id2], cluster_ids)))
    error('id1 (%d) and id2 (%d) must be cluster IDs.', id1, id2);
end

m = max(cluster_ids);
times_CSC.cluster_class(times_CSC.cluster_class(:, 1) == id1) = m+1;
times_CSC.cluster_class(times_CSC.cluster_class(:, 1) == id2) = id1;
times_CSC.cluster_class(times_CSC.cluster_class(:, 1) == m+1) = id2;

if (isfield(times_CSC, 'comments'))
    tmp = times_CSC.comments{id1};
    times_CSC.comments{id1} = times_CSC.comments{id2};
    times_CSC.comments{id2} = tmp;
end
