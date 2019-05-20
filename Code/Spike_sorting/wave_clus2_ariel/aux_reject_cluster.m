function aux_reject_cluster(button_num, aux_num, handles)
% aux_reject_cluster    

% Author: Ariel Tankus.
% Created: 13.06.2006.


button_str = num2str(button_num);
aux_str = num2str(aux_num);

set(gcbo,'value',1);
set(handles.(['isi' button_str '_accept_button']), 'value', 0);
USER_DATA = get(handles.(['wave_clus_aux', aux_str]),'userdata');
classes = USER_DATA{6};
classes(find(classes==button_num))=0;
USER_DATA{6} = classes;
USER_DATA{9} = classes;
par = USER_DATA{1};
par.(['fix', button_str]) = 0;
USER_DATA{1} = par;
h_figs=get(0,'children');
h_fig = findobj(h_figs,'tag','wave_clus_figure');
h_fig1 = findobj(h_figs,'tag',['wave_clus_aux', num2str(1-aux_num)]);
set(handles.(['wave_clus_aux', aux_str]),'userdata',USER_DATA);
set(h_fig,'userdata',USER_DATA)
set(h_fig1,'userdata',USER_DATA)
axes(handles.(['spikes', button_str])); 
cla reset
axes(handles.(['isi', button_str])); 
cla reset
set(gcbo,'value',0);
set(handles.(['isi', button_str, '_accept_button']), 'value', 1);
