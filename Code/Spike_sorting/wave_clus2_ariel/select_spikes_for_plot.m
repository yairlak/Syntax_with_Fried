function display_spikes = select_spikes_for_plot(spikes, num_spikes)
% select_spikes_for_plot    

% Author: Ariel Tankus.
% Created: 09.06.2006.


if (num_spikes > size(spikes, 1))
    error(sprintf('num_spikes (%d) larger than total no. of spikes (%d)', ...
                num_spikes, size(spikes, 1)));
end

% get max and min of every spikes.
max_val = max(spikes, [], 2);
min_val = min(spikes, [], 2);

max_rows = sortrows([max_val, spikes]);
min_rows = sortrows([min_val, spikes]);
if (num_spikes > 1)
    upper_ind = floor((num_spikes+1)./2);
    display_spikes = [max_rows((end-upper_ind+1):end, 2:end)
                      min_rows(1:(num_spikes-upper_ind), 2:end)];
else
    % num_spikes == 1
    display_spikes = max_rows(1, 2:end);
end
