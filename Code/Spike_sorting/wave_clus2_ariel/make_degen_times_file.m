function [] = make_degen_times_file(times_filename, handles)
% make_degen_times_file    

% Author: Ariel Tankus.
% Created: 05.12.2005.


par = handles.par;

spikes = zeros(1, 64);               % silent spike (a.k.a DC).
cluster_class = [0, 0];              % [cluster#, index_of_spike(=time in sec.)]
inspk = zeros(1, par.inputs);        % input wavelet features.
save(times_filename, 'cluster_class', 'spikes', 'inspk', 'par');
