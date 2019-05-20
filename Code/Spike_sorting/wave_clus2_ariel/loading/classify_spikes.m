function [] = classify_spikes(inspk, spikes, spike_times_ms, par, fname_suffix)
% classify_spikes    Classify spike features using Super Paramagnetic
%                    Clustering (SPC).  The results are saved as a
%                    times_* file.
%
%                    classify_spikes(inspk, handles)
%                    inspk - nxk - features of n spikes.  Each feature
%                                  vector is of length k.
%                    handles - struct - should contain the field `par'.

% Author: Ariel Tankus.
% Created: 05.09.2008.


orig_prefix = par.fname;
par.fname = [par.fname, '_', fname_suffix];
par.fname_in = par.fname;     % for v1.1.

%Interaction with SPC
save(par.fname, 'inspk', '-ascii');

handles.par = par;
[clu, tree1] = run_cluster(handles);

temp = find_temp(tree1, handles);                % Selects temperature.
classes = rm_small_clusters(clu(temp, 3:end) + 1, par.min_clus);
cluster_class = [classes', spike_times_ms];

% create empty comments:
num_clusters = length(unique(setdiff(cluster_class(:, 1), 0)));
comments = repmat({''}, num_clusters, 1);

par.fname = orig_prefix;
par.fname_suffix = fname_suffix;

save(['times_', fname_suffix], 'cluster_class', 'spikes', 'inspk', 'par', ...
     'comments');
