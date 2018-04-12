function plot_all_units_entire_experiment(spike_data_all_units, unit_names, trial_times, settings)
params.start_time = 1.945e6; % Sentence block start time
params.end_time = max(cellfun(@max, spike_data_all_units)); % time of latest spike in the experiment
params.window_size = 1e5; % Window size to plot in the GUI

%% 
f = figure('Position',[100,100,1000,500], 'color', [1 1 1]);
myhandles = guihandles(f);
myhandles.params = params;
myhandles.trial_times = trial_times;
myhandles.settings = settings;

%% Draw spikes
for unit = settings.units
    curr_spike_times = spike_data_all_units{unit}; % Spike timings in the i'th unit
    num_spikes   = length(curr_spike_times); % number of spikes
    for spike = 1:num_spikes % for every spike
        % draw a black vertical line of length 1 at time t, at unit j
        line([curr_spike_times(spike), curr_spike_times(spike)],[unit-settings.line_size/2 unit+settings.line_size/2],'Color','k'); 
    end
     xlim([params.start_time params.start_time + params.window_size])
    drawnow
end
xlabel('Time [ms]')
% Add unit names from montage on the y-axis
set(gca, 'ytick', settings.units, 'yticklabel', unit_names(settings.units,2))

%% UI controls
% Add a slider and 'listen' to it
hplot = gca();
myhandles.sld = uicontrol('style','slider','Min',0,'Max',params.end_time,'Value',params.start_time,'SliderStep',[params.window_size/params.end_time/10 params.window_size/params.end_time/2],'units','pixel','position',[300 5 350 15]);
addlistener(myhandles.sld,'ActionEvent',@(hObject, event) makeplot(hObject,event, hplot));
% Add a textbox and a label for shifting the stimulus onsets
myhandles.txtbox_shift = uicontrol(f,'Style','edit', 'String','0', 'Max',1,'Min',0, 'Position',[10 40 50 30]);
myhandles.label_shift = uicontrol(f,'Style','text', 'String','msec', 'Position',[60 40 35 30], 'BackGroundColor', [1 1 1]);
% Add button to apply shift
myhandles.pb = uicontrol(f,'Style','pushbutton','String','Shift onsets','Position',[10 5 100 30], 'Callback', @pb_Callback);

%% Add vertical red lines for stimulus onsets
y_lim = get(gca, 'YLim');
for tr = 1:length(myhandles.trial_times)
    curr_trial = trial_times(tr);
    myhandles.h_lines(tr) = line([curr_trial curr_trial], y_lim, 'color', 'r', 'LineWidth', 2, 'LineStyle', '--');
end

%% Enable zoom
set(f, 'ToolBar', 'figure');  
h = zoom;
h.ActionPreCallback = @myprecallback;
h.ActionPostCallback = @mypostcallback;
h.Enable = 'on';

guidata(f,myhandles)
end

function mypostcallback(obj,evd)
% What happens when zooming
myhandles = guidata(gcbo);
ha = evd.Axes;
newLim = get(ha, 'XLim');
myhandles.params.window_size = newLim(2)-newLim(1);
set(myhandles.sld,'SliderStep',[myhandles.params.window_size/myhandles.params.end_time/10 myhandles.params.window_size/myhandles.params.end_time/2])
set(myhandles.sld,'Value', newLim(1))
ylim([-0.5+myhandles.settings.units(1) myhandles.settings.units(end)+0.5])
guidata(gcbo,myhandles)

end

function makeplot(hObject,event,hplot)
% Update plot in GUI when slider value is modified
myhandles = guidata(gcbo);

myhandles.params.curr_x_lim = get(hplot,'XLim');
myhandles.params.curr_x_lim = myhandles.params.curr_x_lim(1);
xlim([get(hObject, 'Value') get(hObject, 'Value') + myhandles.params.window_size])

drawnow;
guidata(gcbo,myhandles)
end

function pb_Callback(hObject, eventdata, handles)
% Shift stimulus onsets (red lines) when pressing the button 
myhandles = guidata(gcbo);
shift = str2double(get(myhandles.txtbox_shift, 'String'));
y_lim = get(gca, 'YLim');
for tr = 1:length(myhandles.trial_times)
    delete(myhandles.h_lines(tr))
    curr_trial = myhandles.trial_times(tr) + shift;
    myhandles.h_lines(tr) = line([curr_trial curr_trial], y_lim, 'color', 'r', 'LineWidth', 2, 'LineStyle', '--');
end

guidata(gcbo,myhandles)
end