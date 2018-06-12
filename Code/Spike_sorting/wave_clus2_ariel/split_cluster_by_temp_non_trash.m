function [cluster_class, spikes, inspk, par, comments] = ...
    split_cluster_by_temp_non_trash(ch)
% split_cluster_by_temp_all    

% Author: Ariel Tankus.
% Created: 12.11.2009.


temp = 18;
[success, err_msg, classes, index, spikes, par, clu, tree, inspk, ...
         comments] = batch_load_csc_pre_clustered(ch);
if (~success)
    fprintf(err_msg);
    cluster_class = zeros(0, 2);
    return;
end

% save original clustering:
orig_classes = classes;

[classes, index, spikes, inspk, par, comments] = split_cluster_by_temp(temp, ...
    classes, index, spikes, par, clu, tree, inspk, comments);

% remove trash waveforms from classes:
classes(orig_classes == 0) = 0;

cluster_class = [classes, index'];
