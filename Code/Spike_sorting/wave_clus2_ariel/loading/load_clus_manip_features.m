function [h, feature_handles, h_fname, h_all_spikes, h_all_spikes_avg] = ...
    load_clus_manip_features()
% load_clus_manip    Load a new instance of clus_manip.fig (GUI for
%                    manipulation of spike clusters).
%
%                    [h, spikes_handles, isi_handles] = load_clus_manip
%                    h - 1x1 - handle to the clus_manip figure.
%                    feature_handles - 1xn - handles to the feature axes.
%                    h_fname         - 1x1 - handle to file_name text label.
%
%                    See also: plot_spikes_by_clusters, load_clus_manip.

% Author: Ariel Tankus.
% Created: 02.02.2006.


num_feature_axes = 18;

h = hgload('clus_manip_features.fig');
handles = guihandles(h);
feature_handles = zeros(1, num_feature_axes);
for i=1:num_feature_axes
    feature_handles(i) = handles.(['axes', num2str(i)]);
end

h_fname = handles.file_name;
h_all_spikes = handles.all_spikes;
h_all_spikes_avg = handles.all_spikes_avg;
