function times_CSC = rm_range_max_spikes(times_CSC, cl, range_t, range_y)
% rm_range_max_spikes    Remove spikes whose maximum in a certain part of the
%                        spike waveform is within a range of values.
%
%                   times_CSC = rm_range_spikes(times_CSC, range_t, range_y)
%                   times_CSC - struct - see load_save_time_CSC.
%                   cl      - 1x1 - class number.  Only elements from this
%                                   class will be considered.
%                   range_t - 1x2 - [start_t, end_t] - the time t is index
%                                   into the spike waveform.  (e.g., in a 64
%                                   samples waveform: t is in 1:64).
%                   range_y - 1x2 - [start_y, end_y] - range into the waveform
%                                   observations.
%
%                   See also: load_save_time_CSC, rm_high_spikes,
%                             rm_low_spikes, move_high_spikes.

% Author: Ariel Tankus.
% Created: 06.02.2006.


max_spikes = max(times_CSC.spikes(:, range_t(1):range_t(2)), [], 2);
f = find((times_CSC.cluster_class(:, 1) == cl) & (max_spikes >= range_y(1)) &...
         (max_spikes <= range_y(2)));
times_CSC.cluster_class(f, 1) = 0;

times_CSC = compress_cluster_numbers(times_CSC);
