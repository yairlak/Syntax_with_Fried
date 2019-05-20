function times_CSC = rm_low_spikes(times_CSC, cl, th)
% rm_low_spikes    

% Author: Ariel Tankus.
% Created: 06.02.2006.


f = find((times_CSC.cluster_class(:, 1) == cl) & ...
         (min(times_CSC.spikes, [], 2) < th));
times_CSC.cluster_class(f, 1) = 0;

times_CSC = compress_cluster_numbers(times_CSC);
