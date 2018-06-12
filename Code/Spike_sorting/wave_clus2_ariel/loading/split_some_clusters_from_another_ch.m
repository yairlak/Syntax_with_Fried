function [] = split_some_clusters_from_another_ch(ch_cl, cur_fict_ch)
% split_some_clusters_from_another_ch    Split several clusters in several
%                                 channels according to the clustering in
%                                 fictitious times_CSC%d.mat files.
%
%                                 split_some_clusters_from_another_ch(ch_cl,
%                                                                  cur_fict_ch)
%                                 ch_cl - nx2 - cell - {ch, cl_vec} where:
%                                                      ch: channel number.
%                                                      cl_vec: vector of
%                                                          cluster numbers in
%                                                          that channel.
%                                 cur_fict_ch  - 1x1 - fictitious channel
%                                                      number for the first
%                                                      cluster [1000].
%
%                                 See also: split_cluster_from_another_ch,
%                                           cluster_to_spikes_file,
%                                           some_clusters_to_spikes_file,
%                                           split_cluster_from_another_ch,
%                                           ariel_do_clustering_csc,
%                                           merge_clusters.

% Author: Ariel Tankus.
% Created: 06.02.2006.


if (nargin < 2)
    cur_fict_ch = 1000;
end

for i=1:size(ch_cl, 1)
    for j=1:length(ch_cl{i, 2})
        split_cluster_from_another_ch(ch_cl{i, 1}, ch_cl{i, 2}(j), cur_fict_ch);
        fprintf('Channel %d, cluster %d <--| fictitious channel %d\n', ...
                ch_cl{i, 1}, ch_cl{i, 2}(j), cur_fict_ch);
        cur_fict_ch = cur_fict_ch + 1;
    end
end
