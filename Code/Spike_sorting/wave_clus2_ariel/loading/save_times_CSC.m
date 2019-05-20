function [] = save_times_CSC(ch, times_CSC)
% save_times_CSC    

% Author: Ariel Tankus.
% Created: 20.02.2006.



% convert from struct
spikes        = times_CSC.spikes;  
cluster_class = times_CSC.cluster_class;
par           = times_CSC.par;     
inspk         = times_CSC.inspk;

save_vars = {'spikes', 'cluster_class', 'par', 'inspk'};

filename = sprintf('times_CSC%d.mat', ch);
if (isfield('times_CSC', 'comments'))
    comments = times_CSC.comments;
    save_vars = [save_vars, {'comments'}];
end
if (isfield('times_CSC', 'time0'))
    time0 = times_CSC.time0;
    save_vars = [save_vars, {'time0'}];
end
if (isfield('times_CSC', 'timeend'))
    timeend = times_CSC.timeend;
    save_vars = [save_vars, {'timeend'}];
end

save(filename, save_vars{:});
