function merge_spikes_files(spikes_file1, spikes_file2, time_offset2_ms, ...
            out_spikes_file)
% merge_spikes_files    

% Author: Ariel Tankus.
% Created: 14.08.2009.


exist1 = exist(spikes_file1, 'file');
exist2 = exist(spikes_file2, 'file');
if (~exist1 && ~exist2)
    return;
end
if (~exist1 && exist2)
    [success, message, messageid] = copyfile(spikes_file2, out_spikes_file);
    if (~success)
        error('Cannot copy %s to %s (%s)', spikes_file2, out_spikes_file, ...
              message);
    end
    return;
end
if (exist1 && ~exist2)
    [success, message, messageid] = copyfile(spikes_file1, out_spikes_file);
    if (~success)
        error('Cannot copy %s to %s (%s)', spikes_file1, out_spikes_file, ...
              message);
    end
    return;
end

% both files exist; merge them.

load(spikes_file2);
index2  = index;
spikes2 = spikes;

load(spikes_file1);

[index_merged, spikes_merged] = merge_spikes(index, spikes, ...
            index2, spikes2, time_offset2_ms);

index  = index_merged;
spikes = spikes_merged;

save(out_spikes_file, 'index', 'spikes');
