function [] = fictitious_electrode_info(ch_cl, first_fict_ch)
% fictitious_electrode_info    

% Author: Ariel Tankus.
% Created: 29.07.2012.


elec_info = ['.', filesep, 'electrode_info.mat'];
if (~exist(elec_info, 'file'))
    return;
end

load(elec_info);
[status, message, messageid] = movefile(elec_info, [elec_info, '.bkp_fict']);
if (status == 0)
    error('Cannot back %s up: %s', elec_info, message);
end

prev_fict_ch = first_fict_ch;  % the last fictitious channel ID used so far.
for i=1:size(ch_cl, 1)
    
    end_fict_ch = prev_fict_ch + length(ch_cl{i, 2}) - 1;
    cur_inds = prev_fict_ch:end_fict_ch;
    
    if (prod(size(num_samples)) > 1)
        num_samples(cur_inds) = num_samples(ch_cl{i, 1});
        period(cur_inds)       = period(ch_cl{i, 1});
        samp_freq_hz(cur_inds) = samp_freq_hz(ch_cl{i, 1});
        time0(cur_inds)        = time0(ch_cl{i, 1});
        timeend(cur_inds)      = timeend(ch_cl{i, 1});
    end
    
    prev_fict_ch = end_fict_ch + 1;
    
end

save(elec_info, 'bytes_per_samp', 'infile', 'num_samples', 'time0', ...
     'chunk_size', 'nchan', 'period', 'timeend', 'enum', 'num_chunks', ...
     'samp_freq_hz');
