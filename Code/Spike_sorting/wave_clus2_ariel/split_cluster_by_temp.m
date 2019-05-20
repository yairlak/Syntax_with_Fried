function [classes, index, spikes, inspk, par, comments] = ...
    split_cluster_by_temp(temp, classes, index, spikes, par, clu, tree, ...
            inspk, comments)
% split_cluter_by_temp    

% Author: Ariel Tankus.
% Created: 24.10.2009.



%classes = clu(temp,3:end)+1;
% ARIEL: 2009-11-11: length(index) may be greater than size(clu, 2)-2, because
% the later appears to be limited to 30000:
%new_classes = zeros(1, size(clu, 2)-2);
new_classes = zeros(length(index), 1);
cur_cluster = 2;
for i=temp:-1:1
    % tree(i, 6) refers to cluster #2 in the i-th temperature.
    if ((i == 1) | (i == temp) | ...
        ((tree(i, 6) > tree(i-1, 6)) & (tree(i, 6) >= tree(i+1, 6))))
%        fprintf('i = %d\n', i);
        fix_clusters = find(clu(i, 3:end)+1 == 2);
%        fprintf('    #fix_clusters = %d\n', length(fix_clusters));
        if (~isempty(fix_clusters))
            new_classes(fix_clusters) = cur_cluster;
            cur_cluster = cur_cluster + 1;
        end
    end
end 

% update largest cluster:
first_cluster = find(clu(temp, 3:end)+1 == 1);
%fprintf('    #first_cluster = %d\n', length(first_cluster));
new_classes(first_cluster) = 1;
classes = new_classes;
%classes = zeros(size(classes));   % `classes' should store non-fixed clusters.
                                  % The fixed clusters are taken from
                                  % USER_DATA{9+i}.

classes = force_clustering(classes, par, spikes, inspk);

classes = min_clus_size(classes, par.min_clus);
