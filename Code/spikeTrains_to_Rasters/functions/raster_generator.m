function raster_generator(spike_times, line_size)

num_trials = length(spike_times); % number of trials
for trial = 1:num_trials
    curr_spike_times = spike_times{trial}; % Spike timings in the i'th trial
    num_spikes   = length(curr_spike_times); % number of spikes
    for spike = 1:num_spikes % for every spike
        % draw a black vertical line of length 1 at time t (x) and at trial jj (y)
        line([curr_spike_times(spike), curr_spike_times(spike)],[trial-line_size/2 trial+line_size/2],'Color','k'); 
    end
end
% xlabel('Time (ms)'); % Time is in millisecond
% ylabel('Trial number');

end