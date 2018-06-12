function [tsmin_ind, tsmax_ind, tsmin, tsmax] = ...
    ignore_experiment_breaks(break_ann_behavior, break_onset_time_sec, ...
                             TimeStamps, ts_ind, tsmin_ind, tsmax_ind, ...
                             tsmin, tsmax)
% ignore_experiment_breaks    

% Author: Ariel Tankus.
% Created: 14.01.2015.


%[tsmin_ind, tsmax_ind]

% iterate through all break, and truncate the segments (in tsmin, tsmax)
% accordingly:
for break_ind=1:2:length(break_ann_behavior)
    cur_break_start = break_onset_time_sec(break_ind, 1).*1E6;
    cur_break_stop  = break_onset_time_sec(break_ind+1, 1).*1E6;

    rm_inds = [];
    
    len_tsmin = length(tsmin_ind);
    for s=1:len_tsmin
        if ((cur_break_start <= tsmin(s)) & (tsmax(s) <= cur_break_stop))
            % segment completely contained within break; remove it:
            rm_inds = [rm_inds, s];
        elseif ((cur_break_start <= tsmin(s)) & ...
                (tsmin(s) <= cur_break_stop) & ...
                (cur_break_stop <= tsmax(s)))
            % segment min is contained within the break:
            tsmin_ind(s) = find(TimeStamps{ts_ind} > cur_break_stop, 1, 'first');
        elseif ((tsmin(s) < cur_break_start) & ...
                (cur_break_start <= tsmax(s)) & ...
                (tsmax(s) <= cur_break_stop))
            % segment max is contained within the break:
            tsmax_ind(s) = find(TimeStamps{ts_ind} < cur_break_start, 1, 'last');
        elseif ((tsmin(s) < cur_break_start) & ...
                (cur_break_stop < tsmax(s)))
            % the segment contains the whole break. The segment has to
            % be split:
            tsmin_ind_tmp1 = tsmin_ind(s);
            tsmax_ind_tmp1 = find(TimeStamps{ts_ind} < cur_break_start, 1, 'last');
            tsmin_ind_tmp2 = find(TimeStamps{ts_ind} > cur_break_stop, 1, 'first');
            tsmax_ind_tmp2 = tsmax_ind(s);
            
            tsmin_ind(s) = tsmin_ind_tmp1;
            tsmax_ind(s) = tsmax_ind_tmp1;

            % add the new segment at the end of the tsmin, tsmax vectors:
            tsmin_ind = [tsmin_ind, tsmin_ind_tmp2];
            tsmax_ind = [tsmax_ind, tsmax_ind_tmp2];
        end
    end

    if (~isempty(rm_inds))
        tsmin_ind(rm_inds) = [];
        tsmax_ind(rm_inds) = [];
    end
    
    % sort tsmin_ind, tsmax_ind, to ensure added segments (due to split)
    % are in their right place:
    tsmin_ind = sort(tsmin_ind);
    tsmax_ind = sort(tsmax_ind);
    
    tsmin = TimeStamps{ts_ind}(int64(tsmin_ind));
    tsmax = TimeStamps{ts_ind}(int64(tsmax_ind));
end

%[tsmin_ind, tsmax_ind]
