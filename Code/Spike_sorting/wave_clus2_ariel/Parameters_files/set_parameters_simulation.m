function par = set_parameters_simulation(sr,filename,handles, timetotal)

par = set_parameters_simulation_core(sr, filename, timetotal);

USER_DATA = get(handles.wave_clus_figure,'userdata');
USER_DATA{1} = par;
set(handles.wave_clus_figure,'userdata',USER_DATA);
