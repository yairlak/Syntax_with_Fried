function [] = plot_isi_hist(cur_plot, isi, cur_code, par)
% plot_isi_hist    

% Author: Ariel Tankus.
% Created: 03.02.2006.


if (isfield('par', ['bin_step', num2str(cur_code-1)]))
    bin_step = par.(['bin_step', num2str(cur_code-1)]);
else
    bin_step = 1;
end
if (isfield('par', ['nbins', num2str(cur_code-1)]))
    nbins = par.(['nbins', num2str(cur_code-1)]);
else
    nbins = 100;
end

[N, X] = hist(isi, 0:bin_step:nbins);
bar(cur_plot, X(1:end-1),N(1:end-1));
axis(cur_plot, 'tight');

num_spikes_cur_cluster = length(isi) + 1;     % +1: isi is diff. 
% The title it 2.5.*bin_step milliseconds, because the first bin is:
% [-Inf, bin_step/2], the second: (bin_step/2, 1.5*bin_step], the third:
% (1.5*bin_step, 2.5*bin_step].
title(cur_plot, sprintf('%d (%.2f%%)  in < %gms', sum(N(1:3)), ...
            sum(N(1:3)) ./ num_spikes_cur_cluster .* 100, 2.5.*bin_step));
