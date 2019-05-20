function tbl = spikes_per_temperature_table(num_ch)
% spikes_per_temperature_table    

% Author: Ariel Tankus.
% Created: 11.11.2009.


tbl = NaN(num_ch, 2);
tbl(:, 1) = (1:num_ch)';

for i=1:num_ch
    fname = sprintf('data_ch%d.dg_01.lab', i);
    if (~exist(fname, 'file'))
        continue;
    end
    a = load(fname);
    tbl(i, 2) = size(a, 2);
end
