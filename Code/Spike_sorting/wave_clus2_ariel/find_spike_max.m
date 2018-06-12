function [index, nspk] = find_spike_max(xf, xaux)
% find_spike_max    

% Author: Ariel Tankus.
% Created: 02.09.2008.


nspk = 0;
index = [];

cons_table = split_into_consecutive(xaux);

for i=1:size(cons_table, 1)

    cur_xf = xf(xaux(cons_table(i, 1)):xaux(cons_table(i, 2)));
    
    if (length(cur_xf) <= 2)
        [max_xf, peaks] = max(cur_xf);
    else
        % search local maxima:
        d = sign(diff(cur_xf));
        peaks = [strfind(d, [1, -1]), strfind(d, [1, 0])];
        peaks = sort(peaks) + 1;   % +1: to get the exact peak index in xaux.
    end
    
    nspk = nspk + length(peaks);
    index = [index, peaks + xaux(cons_table(i, 1)) - 1];

end
