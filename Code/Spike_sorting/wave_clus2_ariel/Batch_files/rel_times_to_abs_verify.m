function rel_times_to_abs_verify(ch_list)
% rel_times_to_abs_verify    

% Author: Ariel Tankus.
% Created: 15.09.2009.


for i=1:length(ch_list)

    first_time_stamp = read_first_time_stamp(sprintf('CSC%d.Ncs', ch_list(i)));

    times_file = sprintf('./times_CSC%d.mat', ch_list(i));
    if (~exist(times_file, 'file'))
        continue;
    end
    load(times_file);
    cluster_class_abs = cluster_class;
    
    load(sprintf('rel_times_files/times_CSC%d.mat', ch_list(i)));

    % the times are in microsec, so we allow up to 1 micsec error:
    d = abs((cluster_class_abs(:, 2) - cluster_class(:, 2))*1000 - ...
                first_time_stamp);
    if (any(d >= 1))
        fprintf(['%s, Ch: %d: Incompatible abs and relative times (diff range [%d, ' ...
                 ' %d] mic.sec.).\n'], pwd, ch_list(i), range2(round(d)));
    end
    
    clear cluster_class cluster_class_abs;
end
