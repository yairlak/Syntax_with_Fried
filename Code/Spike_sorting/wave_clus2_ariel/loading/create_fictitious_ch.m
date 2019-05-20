function [] = create_fictitious_ch(first_fict_ch)
% create_fictitious_ch    

% Author: Ariel Tankus.
% Created: 19.06.2006.
% Modified: 19.12.2017.  Moved fictitious_electrode_info before clustering,
% so the new electrode_info.mat is created before channels are created and
% spike sorted, thus allowing to start wave_clus as soon as the first file
% was clustered (i.e., CSC1000.mat can be clustered by wave_clus even before
% CSC1001.mat was created).


if (nargin < 1)
    first_fict_ch = 1000;
end

ch_cl = recluster_cut;

fictitious_electrode_info(ch_cl, first_fict_ch);

last_fict_ch = some_clusters_to_spikes_file(ch_cl, first_fict_ch);
ariel_do_clustering_csc(first_fict_ch:last_fict_ch);

fprintf('\nCreated fictitious channels: %d:%d\n', first_fict_ch, last_fict_ch);
