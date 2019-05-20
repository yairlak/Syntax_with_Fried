function times_CSC = plot_low_isi(times_CSC, cl, th)
% plot_low_isi    

% Author: Ariel Tankus.
% Created: 08.02.2006.


if (nargin < 3)
    th = 2.5;     % ms
end

[low_isi_inds, cl_inds] = find_low_isi_inds(times_CSC, cl, th);

for i=1:length(low_isi_inds)
    figure; 
    plot(times_CSC.spikes(cl_inds([low_isi_inds(i), low_isi_inds(i)+1]), :)');
    axis('tight');
    title(sprintf('Spike ind = %d', cl_inds(low_isi_inds(i))));
    legend('First spike', 'Second spike');
end
