function time_offset2_ms = merge_first_last_time_stamps(dir1, dir2, ...
            time_separation_ms, out_dir)
% merge_first_last_time_stamps    Merge the first and last time stamps of two
%                                 sessions.  This is required when converting
%                                 spike_times_to_firing_rates.m.
%
%                                 time_offset2_ms = 
%                                     merge_first_last_time_stamps(dir1, dir2,
%                                         time_offset2_ms, out_dir)
%
%                                 See also:  merge_event_times, merge_spikes,
%                                            merge_spikes_files,
%                                            merge_spikes_sessions.

% Author: Ariel Tankus.
% Created: 15.08.2009.


if (time_separation_ms < 0)
    error('time_separation_ms should be 0 or positive (not: %.f)', ...
          time_separation_ms);
end

filename1 = sprintf('%s/CSC1.Ncs', dir1);
[first_time_stamps1, last_time_stamp1] = ...
    read_first_last_time_stamp(filename1, true);

filename2 = sprintf('%s/CSC1.Ncs', dir2);
[first_time_stamps2, last_time_stamp2] = ...
    read_first_last_time_stamp(filename2, true);

if (first_time_stamps2(1) > last_time_stamp1 + time_separation_ms*1000)
    % the two sessions are separate in time:
    time_offset2_ms = 0;
else
    time_offset2_ms = (last_time_stamp1 - first_time_stamps2(1)) / 1000 + ...
        time_separation_ms;
end

first_time_stamps = first_time_stamps1;
last_time_stamp   = last_time_stamp2 + time_offset2_ms*1000;

save(sprintf('%s/time_stamps_cache.mat', out_dir), 'first_time_stamps', ...
     'last_time_stamp');
