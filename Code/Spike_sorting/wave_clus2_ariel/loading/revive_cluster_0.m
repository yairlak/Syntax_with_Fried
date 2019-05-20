function times_CSC = revive_cluster_0(times_CSC)
% revive_cluster_0    Revive cluster 0 (the trash).  Converts all spikes in
%                     the trash into a single cluster.  Thus, the trash is
%                     left empty after this function.
%
%                     times_CSC = revive_cluster_0(times_CSC)
%                     times_CSC - struct - see load_save_time_CSC.
%
%                     See also: load_save_time_CSC, rm_high_spikes,
%                               rm_low_spikes, move_high_spikes,
%                               rm_range_max_spikes, rm_range_min_spikes.

% Author: Ariel Tankus.
% Created: 09.10.2007.


times_CSC = compress_cluster_numbers(times_CSC);    % just to make sure.

max_cluster_id = max(unique(times_CSC.cluster_class(:, 1)));
f = find(times_CSC.cluster_class(:, 1) == 0);
times_CSC.cluster_class(f, 1) = max_cluster_id + 1;
