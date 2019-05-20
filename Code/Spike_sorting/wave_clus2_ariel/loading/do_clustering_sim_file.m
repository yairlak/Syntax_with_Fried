function [] = do_clustering_sim_file(filename)
% load_sim_file    

% Author: Ariel Tankus.
% Created: 05.09.2008.


load(filename);                      % Load data
x.data=data;
x.sr=1000./samplingInterval;

timetotal = (length(data)-1).*samplingInterval;
par = set_parameters_simulation_core(x.sr,filename,timetotal); % Load parameters
%par.fname = [par.fname, '_', basename];
%set(min_clus_edit,'string',num2str(handles.par.min_clus));

[spikes,thr,index] = amp_detect(x.data, par);     % Detection with amp. thresh.
handles.par = par;
inspk = wave_features(spikes, handles);        % Extract spike features.

spike_times_ms = index'*1000/par.sr;
[pathstr, basename, ext, versn] = fileparts(filename);
classify_spikes(inspk, spikes, spike_times_ms, par, basename);
