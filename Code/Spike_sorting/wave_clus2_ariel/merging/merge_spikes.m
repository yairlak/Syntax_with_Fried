function [index_merged, spikes_merged] = merge_spikes(index1, spikes1, ...
            index2, spikes2, time_offset2_ms)
% merge_spikes_files    

% Author: Ariel Tankus.
% Created: 14.08.2009.


index2 = index2 + time_offset2_ms;

num_samples1 = size(spikes1, 2);
num_samples2 = size(spikes2, 2);

if (num_samples1 ~= num_samples2)
    
    w_pre1  = round(num_samples1 * 20/64);
    w_post1 = round(num_samples1 * 44/64);
    w_pre2  = round(num_samples2 * 20/64);

    [spikes2_interp, inds] = interp_spikes(spikes2, w_pre2, w_pre1, w_post1);
    
    spikes_w_times = [index1', spikes1;
                  index2', spikes2_interp];

else

    spikes_w_times = [index1', spikes1;
                      index2', spikes2];

end

spikes_w_times = sortrows(spikes_w_times, 1);

index_merged  = spikes_w_times(:, 1)';
spikes_merged = spikes_w_times(:, 2:end);
