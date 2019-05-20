function [] = reject_all_clusters(ch_list)
% reject_all_clusters    

% Author: Ariel Tankus.
% Created: 09.08.2006.


for ch=ch_list
    load(sprintf('times_CSC%d.mat', ch));

    cluster_class(:, 1) = 0;

    if (exist('comments', 'var'))
        save(sprintf('times_CSC%d.mat', ch), 'inspk', 'spikes', ...
             'cluster_class', 'par', 'comments');
        clear comments;   % don't copy from one channel to the other (not all
                          % must have comments).
    else
        save(sprintf('times_CSC%d.mat', ch), 'inspk', 'spikes', ...
             'cluster_class', 'par');
    end
end
