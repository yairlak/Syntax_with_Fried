function [] = split_cluster_from_another_ch(orig_ch, orig_cl, fict_ch)
% split_cluster_from_another_ch    

% Author: Ariel Tankus.
% Created: 02.02.2006.
% Modified: 21.10.2007.  Check whether times_CSC file exists.


save_vars = {'cluster_class', 'inspk', 'par', 'spikes'};

times_filename = sprintf('times_CSC%d.mat', fict_ch);
if (~exist(times_filename, 'file'))
    fprintf(['WARNING:  File: %s not found.  Splitting Ch. %d, Sub-Cl. %d '...
             'from Ch. %d skipped!\n'], times_filename, orig_ch, orig_cl, ...
            fict_ch);
    return;
end

load(times_filename);
new_cl = cluster_class(:, 1);
if (exist('comments', 'var'))
    new_comments = comments;
    save_vars = [save_vars, {'comments'}];
    clear comments;    % ensure fict. comments are not mixed with original ones.
end

orig_fname = sprintf('times_CSC%d.mat', orig_ch);
[success, message, messageid] = copyfile(orig_fname, [orig_fname, '.bkp']);
if (~success)
    fprintf('Failed to backup %s, split cancelled:\n%s\nError code: %d', ...
            orig_fname, message, messageid);
    return;
end

load(orig_fname);
cl_inds = find(cluster_class(:, 1) == orig_cl);
if (length(cl_inds) ~= length(new_cl))
    error(sprintf(['Cluster #%d of ch. %d has a different number of spikes ' ...
                   '(%d) than ch. %d (%d).'], orig_cl, orig_ch, ...
                length(cl_inds), fict_ch, length(new_cl)));
end

% new_cl == 0: added to cluster #0 (junk).
% new_cl == 1: replaces the cluster orig_cl (from which the fictitious
%              channel: fict_ch was originated).
% new_cl > 1:  additional channels are added after existing channels.
new_cl_ge1_inds = find(new_cl > 1);
new_cl(find(new_cl == 1)) = orig_cl;
new_cl(new_cl_ge1_inds) = new_cl(new_cl_ge1_inds) + max(cluster_class(:, 1))-1;

if (exist('new_comments', 'var'))
    if (exist('comments', 'var'))
        comments = repmat({''}, length(setdiff(unique(cluster_class(:, 1)), 0)), 1);
    end
    
    % >=2: The first index is the trash.  >=2 means there was at least one
    %      cluster in the new sorting.
    if (length(new_comments) >= 2)
        comments(orig_cl) = new_comments(2);
    end
    if (length(new_comments) > 2)
        comments = [comments; new_comments(3:end)];
    end
end

% actually change cluster numbers:
cluster_class(cl_inds, 1) = new_cl;

if (exist('time0', 'var'))
    save_vars = [save_vars, {'time0'}];
end
if (exist('timeend', 'var'))
    save_vars = [save_vars, {'timeend'}];
end
if (~exist('comments', 'var'))
    save_vars = setdiff(save_vars, 'comments');
end

save(orig_fname, save_vars{:});
