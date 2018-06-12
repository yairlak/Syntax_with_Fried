function [] = plot_cluster_spikes(cur_plot, spikes, total_num_spikes, ...
            time_interval, cluster_codes, cur_code, num_sigmas, avg_state)
% plot_cluster_spikes    
%
%                        avg_state - 1x1 - State defining the plot of
%                                          average:
%                                          0 - Plot cluster with average.
%                                          1 - Plot cluster without average.
%                                          2 - Plot only average.

% Author: Ariel Tankus.
% Created: 03.02.2006.


colors = ['k' 'b' 'r' 'g' 'c' 'm' 'y' 'b' 'r' 'g' 'c' 'm' 'y' 'b'];
gray_color = [0.4, 0.4, 0.4];

cur_color = colors(rem(cur_code-1, length(colors))+1);
if ((avg_state == 0) | (avg_state == 1))
    plot(cur_plot, spikes', cur_color);
end
hold(cur_plot, 'on');     % in avg_state==0, hold for next clusters.
if ((avg_state == 0) | (avg_state == 2))
    mu = nanmean(spikes);
    if (avg_state == 0)
        avg_color = 'k';
    elseif (avg_state == 2)
        avg_color = cur_color;
    end
    plot(cur_plot, mu, avg_color, 'linewidth', 2);
    if (avg_state == 0)
        sigma = nanstd(spikes);
        avup = mu + num_sigmas * sigma;
        avdw = mu - num_sigmas * sigma;
        plot(cur_plot, avup,'color', gray_color, 'linewidth', 0.5);
        plot(cur_plot, avdw, 'color', gray_color, 'linewidth', 0.5);
    end
end

num_spikes_cur_cluster = size(spikes, 1);
title(cur_plot, sprintf('Cluster #%d: %d (%.2f%%)\n%.2fHz', ...
            cluster_codes(cur_code), num_spikes_cur_cluster, ...
            num_spikes_cur_cluster./total_num_spikes.*100, ...
            num_spikes_cur_cluster./time_interval));
axis(cur_plot, 'tight');
