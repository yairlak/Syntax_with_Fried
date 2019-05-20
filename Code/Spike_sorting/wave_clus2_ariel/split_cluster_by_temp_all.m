function [cluster_class, spikes, inspk, par, comments] = ...
    split_cluster_by_temp_all(ch)
% split_cluster_by_temp_all    

% Author: Ariel Tankus.
% Created: 25.10.2009.


temp = 18;
[success, err_msg, classes, index, spikes, par, clu, tree, inspk, ...
         comments] = batch_load_csc_pre_clustered(ch);
if (~success)
    fprintf(err_msg);
    cluster_class = zeros(0, 2);
    return;
end

[classes, index, spikes, inspk, par, comments] = split_cluster_by_temp(temp, ...
    classes, index, spikes, par, clu, tree, inspk, comments);

cluster_class = [classes, index'];
