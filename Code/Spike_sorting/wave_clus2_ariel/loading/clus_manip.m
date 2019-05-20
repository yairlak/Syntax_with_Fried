function [h1, h_feat1] = clus_manip(ch, times_prefix)
% clus_manip    Plot the spikes in a times_CSC file, according to their
%               clustering.
%
%               plot_spikes_by_clusters(ch)
%               ch - 1x1 - channel number.  The times_CSC file must reside in
%                          the current working directory.
%               or:
%               ch - string - The file times_`ch' should exist in cur. dir.
%               times_prefix - string - prefix of the times file ['times'].
%
%               See also: wave_clus, merge_clusters,
%                         split_cluster_from_another_ch.

% Author: Ariel Tankus.
% Created: 21.01.2006.

% cluster_class - nx2 - [cluster_code, spikes_time] - 
% clusters - nx64 - waveforms of the each spike (64 samples of the waveform).


if (nargin < 2)
    times_prefix = 'times';
end

colors = ['k' 'b' 'r' 'g' 'c' 'm' 'y' 'b' 'r' 'g' 'c' 'm' 'y' 'b'];

if (isnumeric(ch))
    filename = sprintf('%s_CSC%d.mat', times_prefix, ch);
else
    filename = sprintf('%s_%s.mat', times_prefix, ch);
end

load(filename);
if (~isfield('par', 'to_plot_std'))
    par.to_plot_std = 1;      % #standard deviations to plot around mean
                              % spike waveform.
end

num_features = size(inspk, 2);
[h_feat, feature_handles, h_all_spikes, h_all_spikes_avg] = ...
    load_some_clus_manip_features(num_features, filename);

[h, spikes_handles, isi_handles, h_fname] = load_clus_manip;
set(h, 'Name', 'Clus_Manip #0');
set(h_fname, 'String', filename);

num_spikes = size(cluster_class, 1);
time_interval = (cluster_class(end, 2) - cluster_class(1, 2)) ./ 1000;

cluster_codes = unique(cluster_class(:, 1));   % unique() also sorts.
if (cluster_codes(1) ~= 0)
    % cluster #0 may be empty.
    cluster_codes = [0; cluster_codes];
end
for i=1:length(cluster_codes)
    spike_inds = find(cluster_class(:, 1) == cluster_codes(i));
    
    cur_plot_ind = rem(i-1, length(spikes_handles))+1;
    cur_plot = spikes_handles(cur_plot_ind);
    plot_cluster_spikes(cur_plot, spikes(spike_inds, :), num_spikes, ...
                time_interval, cluster_codes, i, par.to_plot_std, 0);
    plot_cluster_spikes(h_all_spikes, spikes(spike_inds, :), num_spikes, ...
                time_interval, cluster_codes, i, par.to_plot_std, 1);
    plot_cluster_spikes(h_all_spikes_avg, spikes(spike_inds, :), num_spikes, ...
                time_interval, cluster_codes, i, par.to_plot_std, 2);
    
    isi = diff(cluster_class(spike_inds, 2));
    cur_plot = isi_handles(cur_plot_ind);
    plot_isi_hist(cur_plot, isi, i, par);

    counter = 1;
    for j=1:(num_features - 1)
        for k=(j+1):num_features
            if (counter > length(feature_handles))
                break;
            end
            hold(feature_handles(counter), 'on');
            plot(feature_handles(counter), inspk(spike_inds, j), ...
                 inspk(spike_inds, k), ...
                 ['.', colors(rem(i-1, length(colors))+1)], 'markersize', .5);
            counter = counter + 1;
        end
    end

    if ((rem(i, length(spikes_handles)) == 0) & (i < length(cluster_codes)))
        [h, spikes_handles, isi_handles, h_fname] = load_clus_manip;
        set(h, 'Name', sprintf('Clus_Manip #%d', i./length(spikes_handles)));
        set(h_fname, 'String', filename); 
    end
end

if (nargin > 0)
    h1 = h;
    h_feat1 = h_feat;
end
