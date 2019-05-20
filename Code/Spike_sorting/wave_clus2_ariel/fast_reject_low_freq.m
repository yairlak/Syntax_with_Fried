function [is_rejected, channel_freq] = fast_reject_low_freq(cluster_class, ...
            inspk, par, spikes, times_filename)
% fast_reject_low_freq    

% Author: Ariel Tankus.
% Created: 04.12.2005.


channel_freq = size(spikes, 1) ./ par.timetotal;    % multiunit frequency
is_rejected = (channel_freq < par.min_freq);
if (is_rejected)
    cluster_class(:, 1) = 0;                        % reject all spikes.
    save(times_filename, 'cluster_class', 'inspk', 'par', 'spikes');
end
