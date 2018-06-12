function auto_reject_clusters(cluster_class, inspk, spikes, par, comments)
% auto_reject_clusters    

% Author: Ariel Tankus.
% Created: 04.09.2006.


min_flat_pts = 6;      % At least the first `min_flat_pts' points should have
max_flat_slope = 0.5;  % a slope (=diff) lower than `max_flat_slope' (in abs
                       % value) in order for the initial part of the waveform
                       % to be considered flat.
xRadius = 3;
min_thresh_diff2 = -0.5;  % points with 2nd derivative below this threshold
                          % will be considered concave.

row_length = 2;

cluster_ids = unique(cluster_class(:, 1));

num_clusters = length(cluster_ids);
num_pts_per_spike = size(spikes, 2);
avg_waveform   = zeros(num_clusters, num_pts_per_spike);
diff_waveform  = zeros(num_clusters, num_pts_per_spike-1);
smooth_d       = zeros(num_clusters, num_pts_per_spike-1);
diff2_waveform = zeros(num_clusters, num_pts_per_spike-2);

for i=1:num_clusters
%for i=3

    cluster_inds = find(cluster_class(:, 1) == cluster_ids(i));
    avg_waveform(i, :)   = mean(spikes(cluster_inds, :));
    diff_waveform(i, :)  = diff(avg_waveform(i, :));
    diff2_waveform(i, :) = diff(diff_waveform(i, :));
    
    x = -1:(1/xRadius):1;
    g = gauss(x, 1/3, 0);
    smooth_diff = conv(diff_waveform(i, :), g);
    smooth_d(i, :) = smooth_diff(length(g):end);

    num_concave_pts = length(find(diff2_waveform(i, 13:17) < min_thresh_diff2));
    
    figure;
    subplot(3, row_length, 1);
    plot(avg_waveform(i, :));
    grid on;
    subplot(3, row_length, 1+row_length);
    plot(2:num_pts_per_spike, diff_waveform(i, :));
    grid on;
    subplot(3, row_length, 1+2.*row_length);
    plot(3:num_pts_per_spike, diff2_waveform(i, :));
    grid on;
    subplot(3, row_length, 2+row_length);
    plot(2:num_pts_per_spike, smooth_d(i, :));
    grid on;

    title_text = sprintf('Cluster #%d', cluster_ids(i));

    if (any(abs(diff_waveform(i, 1:min_flat_pts)) > max_flat_slope))
        title_text = [title_text, '- Non-flat init'];
    end
    if (num_concave_pts >= 2)
        title_text = [title_text, '- Concave init'];
    end
    subplot(3, row_length, 1);
    title(title_text);
    
end
