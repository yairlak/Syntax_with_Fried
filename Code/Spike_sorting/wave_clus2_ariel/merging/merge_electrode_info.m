function [] = merge_electrode_info(dir1, dir2, time_offset2_ms, out_dir)
% merge_electrode_info    

% Author: Ariel Tankus.
% Created: 31.07.2010.


cur_wd = pwd;

cd(dir1);
if (exist('./electrode_info.mat', 'file'))
    load electrode_info.mat;
    t_0 = time0;
    t_end = timeend;
    n_samples = num_samples;
    i_file = infile;
end

cd(dir2);
if (exist('./electrode_info.mat', 'file'))
    load electrode_info.mat; 
end

time0 = t_0;
timeend = timeend + time_offset2_ms.*1000;      % microsec.
num_samples = (timeend - time0) ./ 1E6 .* samp_freq_hz + 1;

chunk_size = 2E6;
num_chunks = ceil(num_samples ./ chunk_size);

infile = [i_file, ' MERGED WITH ', infile];

save([out_dir, filesep, 'electrode_info.mat'], 'enum', 'nchan', 'period', ...
     'infile', 'samp_freq_hz', 'bytes_per_samp', 'num_samples', 'chunk_size',...
     'num_chunks', 'time0', 'timeend');

cd(cur_wd);
