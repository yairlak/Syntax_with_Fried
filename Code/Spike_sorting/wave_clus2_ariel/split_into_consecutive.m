function cons_table = split_into_consecutive(xaux)
% split_into_consecutive    Split a vector of sorted indices into
%                           consecutive sequences.
%
%                           cons_table = split_into_consecutive(xaux)
%                           xaux - 1xn or nx1 - sorted vector of numbers.
%                           cons_table  - kx2 - [start, end] - indices of
%                                               starts and ends of consecutive
%                                               sequences in xaux (i.e.,
%                                               a sequence with difference = 1).
%                                               The start and end values
%                                               can be identical if a
%                                               value is not in a consecutive
%                                               sequence.
%
%                           See also: get_entry_exit_inds, find_spike_max.

% Author: Ariel Tankus.
% Created: 03.09.2008.


cons_table = [];

if (~issorted(xaux))
    xaux = sort(xaux);
end

xaux_len = length(xaux);
i = 1;
while (i <= xaux_len)
    % search for consecutive entries in xaux:
    cur_start = i;
    while ((i <= xaux_len - 1) && (xaux(i+1) - xaux(i) == 1))
        i = i + 1;
    end
    cur_end = i;

    cons_table = [cons_table;
                  cur_start, cur_end];
    
    i = i + 1;
end
