% #### Hagar Correction ####
function par=set_parameters_CSC(sr,filename,timetotal,handles)
% function par=set_parameters(sr,filename,handles)
if nargin < 3
    timetotal = 3000;
    fprintf(1,['Warning: the timetotal parameter ' ...
               'was not initialized, use a 3000sec default\n']);
end;

par = set_joint_parameters_CSC(sr);
par.timetotal = timetotal;


% HISTOGRAM PARAMETERS
for i=1:par.max_clus+1
    par.(['nbins', num2str(i-1)]) = 100;  % max bin size for the ISI hist. [ms]
    par.(['bin_step', num2str(i-1)]) = 1; % bin size for the ISI histograms [ms]
end

par.filename = filename;

% Sets to zero fix buttons from aux figures
for i=4:par.max_clus
    eval(['par.fix' num2str(i) '=0;']);
end

if (nargin >= 4)
    % update figure with params:
    USER_DATA = get(handles.wave_clus_figure,'userdata');
    USER_DATA{1} = par;
    set(handles.wave_clus_figure,'userdata',USER_DATA);
end
