function times_CSC = rm_low_isi_spikes(times_CSC, cl, th)
% rm_low_isi_spikes    Remove the spikes whose refractory period is lower
%                      than a given threshold.
%
%                      times_CSC = rm_low_isi_spikes(times_CSC, cl, th)
%                      times_CSC - struct - see load_times_CSC.
%                      cl           - 1x1 - class no.
%                      th           - 1x1 - refrectory period [millisec.].
%
%                      See also: load_times_CSC, save_times_CSC,
%                                load_save_time_CSC, rm_high_spikes,
%                                rm_low_spikes, rm_range_max_spikes,
%                                rm_range_min_spikes.

% Author: Ariel Tankus.
% Created: 20.02.2006.


[low_isi_inds_in_cl, cl_inds] = find_low_isi_inds(times_CSC, cl, th);
times_CSC.cluster_class(cl_inds(low_isi_inds_in_cl+1), 1) = 0;
