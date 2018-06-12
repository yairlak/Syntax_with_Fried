function [] = multiple_detection_same_spike(ch, subcl1, subcl2)
% multiple_detection_same_spike    

% Author: Ariel Tankus.
% Created: 22.01.2014.


load(sprintf('times_CSC%d.mat', ch));

cl1_inds = find(cluster_class(:, 1) == subcl1);
cl2_inds = find(cluster_class(:, 1) == subcl2);

num_spikes1 = length(cl1_inds);
num_spikes2 = length(cl2_inds);

if (num_spikes1 <= num_spikes2)
    min_inds = cl1_inds;
    max_inds = cl2_inds;
    min_cl = subcl1;
    max_cl = subcl2;
else
    min_inds = cl2_inds;
    max_inds = cl1_inds;
    min_cl = subcl2;
    max_cl = subcl1;
end

min_dists     = NaN(length(min_inds), 1);
min_dist_inds = NaN(length(min_inds), 1);

for i=1:length(min_inds)
    [min_dists(i), min_dist_inds(i)] = min(abs(cluster_class(max_inds, 2) - ...
                                               cluster_class(min_inds(i), 2)));
end

spike_duration_ms = (par.w_pre + par.w_post) ./ par.sr .* 1000;

if (min(min_dists) <= spike_duration_ms)
    same_spike_inds = find(min_dists <= spike_duration_ms);
    num_same_spike = length(same_spike_inds);
    fprintf('Same spike detected multiple times in %d cases:\n', ...
            num_same_spike);
    same_spike_table = [min_cl.*ones(num_same_spike, 1), same_spike_inds, ...
                        max_cl.*ones(num_same_spike, 1), min_dist_inds(same_spike_inds), ...
                        min_dists(same_spike_inds)];
    fprintf('Cl %d: %d,   Cl %d: %d,   dist=%.2gms\n', same_spike_table');
else
    fprintf('All detected spikes are different!\n');
end
