function ts = index_to_sample_time(index, rec_min, TimeStamps)
% index_to_sample_time    

% Author: Ariel Tankus.
% Created: 24.07.2009.


if (isempty(index))
    ts = [];
    return;
end

rec_ind = floor((index-1) ./ 512);
abs_rec_ind = rec_min + rec_ind;

local_dt = zeros(1, length(abs_rec_ind));

% indices of abs_rec_ind which are smaller than the last index:
abs_rec_ind_not_last = (abs_rec_ind < length(TimeStamps));
if (any(abs_rec_ind_not_last))
    local_dt(abs_rec_ind_not_last) = ...
        TimeStamps(abs_rec_ind(abs_rec_ind_not_last)+1) - ...
        TimeStamps(abs_rec_ind(abs_rec_ind_not_last));
end

% indices of abs_rec_ind which are equal to the last index:
abs_rec_ind_last = (abs_rec_ind == length(TimeStamps));
if (any(abs_rec_ind_last))
    local_dt(abs_rec_ind_last) = ...
        TimeStamps(abs_rec_ind(abs_rec_ind_last)) - ...
        TimeStamps(abs_rec_ind(abs_rec_ind_last)-1);
end

% The index within the current record:
index_rel_to_rec = index - rec_ind*512;

if (max(abs_rec_ind) > length(TimeStamps))
    keyboard
end
ts = TimeStamps(abs_rec_ind)' + (index_rel_to_rec-1).*local_dt./512;
