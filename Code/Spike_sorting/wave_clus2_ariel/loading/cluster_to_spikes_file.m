function [] = cluster_to_spikes_file(ch, cl, target_spikes_file_num)
% cluster_to_spikes_file    Save a cluster in a separate spikes file.
%                           This allows running Do_clustering_CSC on the
%                           cluster itself.
%
%                           cluster_to_spikes_file(ch, cl, ...
%                                                  target_spikes_file_num)
%                           ch - 1x1 - channel number.
%                           cl - 1x1 - cluster number of channel ch.
%                           target_spikes_file_num - 1x1 - the number of
%                                      fictitious channel number to allocate
%                                      for the new CSC_spikes file.
%                                      This will usually exceed the number of
%                                      channels in a recording (currently 64).
%
%                           See also: plot_spikes_by_clusters,
%                                     merge_clusters,
%                                     split_cluster_from_another_ch,
%                                     ariel_do_clustering_csc.

% Author: Ariel Tankus.
% Created: 02.02.2006.
% Modified: 05.09.2008.  Allow string or cell for `ch'.


if (strcmp(class(ch), 'double'))
    load(sprintf('times_CSC%d.mat', ch));
elseif (strcmp(class(ch), 'char'))
    load(sprintf('times_%sd.mat', ch));
elseif (strcmp(class(ch), 'cell'))
    load(sprintf('times_%sd.mat', ch{1}));
end

inds = find(cluster_class(:, 1) == cl);

spikes = spikes(inds, :);           % spike waveform.
index  = cluster_class(inds, 2);     % spike times.

target_file = sprintf('.%sCSC%d_spikes.mat', filesep, target_spikes_file_num);
if (exist(target_file, 'file'))
    error([target_file ' already exists.']);
end
save(target_file, 'index', 'spikes');
if (isunix)
    [s, w] = unix(sprintf('ln_fictitious_ch %d %d', ch, ...
                target_spikes_file_num));
    if (s ~= 0)
        fprintf('%s\n', w);
    end
else
    orig_file_ncs = sprintf('.%sCSC%d.Ncs', filesep, ch);
    if (exist(orig_file_ncs, 'file'))
        target_fname = sprintf('CSC%d.Ncs', target_spikes_file_num);
    else
        orig_file = sprintf('.%sCSC%d.mat', filesep, ch);
        if (exist(orig_file, 'file'))
            target_fname = sprintf('CSC%d.mat', target_spikes_file_num);
        else
            error('Original flies %s or %s does not exist.', orig_file_ncs, ...
                  orig_file);
        end
    end
    if (exist(target_fname, 'file'))
        error([target_fname ' already exists.']);
    end
    fid = fopen(target_fname, 'w');
    if (fid == -1)
        error('Cannot open %s for write.', target_fname);
    end
    fclose(fid);
end
