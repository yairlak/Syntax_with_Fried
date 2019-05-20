function [] = plot_single_cluster_waveform(cl)
% plot_single_cluster_waveform    

% Author: Ariel Tankus.
% Created: 09.11.2006.


[ch, sub_cl] = cl_to_ch_sub_cl(cl);
load(sprintf('times_CSC%d', ch));
inds = find(cluster_class(:, 1) == sub_cl);

figure
hold on;

for i=1:length(inds)
    plot(spikes(inds(i), :))
end

mean_waveform = mean(spikes(inds, :));
std_waveform =  std(spikes(inds, :));

plot(mean_waveform, 'k', 'LineWidth', 3);
plot(mean_waveform + std_waveform, 'Color', [0.3, 0.3, 0.3], 'LineWidth', 1.5);
plot(mean_waveform - std_waveform, 'Color', [0.3, 0.3, 0.3], 'LineWidth', 1.5);
set(gca, 'XLim', [1, length(mean_waveform)]);
set(gca, 'YLim', [min(min(spikes(inds, :))), max(max(spikes(inds, :)))]);
