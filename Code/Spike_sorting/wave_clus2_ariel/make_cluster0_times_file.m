function [] = make_cluster0_times_file(times_filename, handles, ch)
% make_cluster0_times_file    

% Author: Ariel Tankus.
% Created: 29.08.2007.


par = handles.par;

load(sprintf('CSC%d_spikes.mat', ch));

num_spikes = size(spikes, 1);
%  [cluster#, index_of_spike(=time in sec.)]
cluster_class = [zeros(num_spikes, 1), index'*1E-6];
inspk = zeros(num_spikes, par.inputs);        % input wavelet features.
save(times_filename, 'cluster_class', 'spikes', 'inspk', 'par');
