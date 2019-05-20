function [h, spikes_handles, isi_handles, h_fname] = load_clus_manip()
% load_clus_manip    Load a new instance of clus_manip.fig (GUI for
%                    manipulation of spike clusters).
%
%                    [h, spikes_handles, isi_handles] = load_clus_manip
%                    h - 1x1 - handle to the clus_manip figure.
%                    spikes_handles - 1xn - handles to the spikes axes
%                                           (ordered 0 to 3).
%                    isi_handles    - 1xn - handles to the inter-spike interval
%                                           (ISI) axes (ordered 0 to 3).
%                    h_fname        - 1x1 - handle to file_name text label.
%
%                    See also: plot_spikes_by_clusters2.

% Author: Ariel Tankus.
% Created: 02.02.2006.


h = hgload('clus_manip.fig');
handles = guihandles(h);
spikes_handles = [handles.spikes0, handles.spikes1, handles.spikes2, ...
                  handles.spikes3];
isi_handles    = [handles.isi0, handles.isi1, handles.isi2, handles.isi3];
h_fname        = handles.file_name;
