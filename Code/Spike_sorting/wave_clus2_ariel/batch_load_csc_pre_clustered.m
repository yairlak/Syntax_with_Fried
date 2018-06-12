function [success, err_msg, classes, index, spikes, par, clu, tree, inspk, ...
         comments] = batch_load_csc_pre_clustered(ch)
% batch_load_csc_pre_clustered    

% Author: Ariel Tankus.
% Created: 24.10.2009.


% inspk and comments may not exist in all files:
comments = {};
inspk    = {};
classes  = zeros(0, 1);
index    = zeros(0, 1);
spikes   = [];
par      = [];
clu      = [];
tree     = [];

filename = sprintf('CSC%d.Ncs', ch);
if (~exist(filename, 'file'))
    err_msg = sprintf('File %s not found', filename);
    success = false;
    return;
end

[time0, timeend, sr, timetotal] = read_main_time_stamps(filename);
par = set_parameters_CSC(sr, filename, timetotal);   % Load parameters

times_filename = ['times_CSC', num2str(ch), '.mat'];
if (~exist(times_filename, 'file'))
    err_msg = sprintf('File %s not found', times_filename);
    success = false;
    return;
end
load(times_filename);

index = cluster_class(:,2)';
fname = ['data_ch' num2str(ch)];           %filename for interaction with SPC
lab_filename = [fname, '.dg_01.lab'];
if (~exist(lab_filename, 'file'))
    err_msg = sprintf('File %s not found', lab_filename);
    success = false;
    return;
end
clu = load(lab_filename);
dg_filename = [fname, '.dg_01'];
if (~exist(lab_filename, 'file'))
    err_msg = sprintf('File %s not found', dg_filename);
    success = false;
    return;
end
tree = load(dg_filename); 

if (exist('cluster_class', 'var'))
    % already manually classified
    classes = cluster_class(:, 1)';    % override prev. def.
else
    if size(clu,2)-2 < size(spikes,1);
        classes = clu(temp,3:end)+1;
        classes = [classes(:)' zeros(1,size(spikes,1)-handles.par.max_spk)];
    else
%%% THIS PART IS BUGGY: See A14-ch45:  classes should have the size of
%                                      `spikes', even if `clu' is larger.
        classes = clu(temp,3:end)+1;
    end
end

success = true;
err_msg = [];
