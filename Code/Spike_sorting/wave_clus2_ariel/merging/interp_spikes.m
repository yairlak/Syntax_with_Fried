function [spikes_interp, new_inds] = interp_spikes(spikes, w_pre, new_w_pre, ...
            new_w_post)
% interp_spikes    

% Author: Ariel Tankus.
% Created: 14.08.2009.


[num_spikes, num_samples] = size(spikes);

pre_inds  = linspace(1, w_pre, new_w_pre);
post_inds = linspace(w_pre, num_samples, new_w_post+1);
post_inds = post_inds(2:end);    % discard first index, which repeats
                                 % last of w_pre.

new_inds = [pre_inds, post_inds];
spikes_interp = zeros(num_samples, new_w_pre + new_w_post);
for i=1:num_spikes
    spikes_interp(i, :) = interp1(1:num_samples, spikes(i, :), new_inds);
end
