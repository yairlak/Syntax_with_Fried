function times_CSC = move_high_spikes(times_CSC, cl_orig, th, cl)
% rm_high_spikes    

% Author: Ariel Tankus.
% Created: 06.02.2006.


f = find((times_CSC.cluster_class(:, 1) == cl_orig) & ...
         (max(times_CSC.spikes, [], 2) > th));
times_CSC.cluster_class(f, 1) = cl;

times_CSC = compress_cluster_numbers(times_CSC);
