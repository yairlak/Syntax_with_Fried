function plot_spikes(handles)
USER_DATA = get(handles.wave_clus_figure,'userdata');
if (isempty(USER_DATA))
    warndlg(sprintf('No data found.\nLoad data first.'), 'Warning', 'replace');
    return;
end
par = USER_DATA{1};
spikes = USER_DATA{2};
spk_times = USER_DATA{3};
clu = USER_DATA{4};
classes = USER_DATA{6};
classes = classes(:)';
inspk = USER_DATA{7};
temp = USER_DATA{8};
[num_spikes, ls] = size(spikes);
par.to_plot_std = 1;                % # of std from mean to plot

% Closes aux figures
h_figs=get(0,'children');
h_fig = findobj(h_figs,'tag','wave_clus_figure');
h_fig1 = findobj(h_figs,'tag','wave_clus_aux0');
h_fig2= findobj(h_figs,'tag','wave_clus_aux1');
close(h_fig1); close(h_fig2);
h = findobj(get(0, 'children'), 'flat', 'name', 'All features');
if (ishandle(h))
    close(h);
end

% Extract spike features if needed
%if get(handles.spike_shapes_button,'value') ==0
    if isempty(inspk) | (length(inspk)~=num_spikes)
        [inspk] = wave_features_wc(spikes,handles);        
        USER_DATA{7} = inspk;
    end
%end

% Defines nclusters
cluster_sizes = zeros(1, par.max_clus);
for i=1:par.max_clus
    cluster_sizes(i) = length(find(classes==i));
end
nclusters = length(find(cluster_sizes(:) >= par.min_clus));

% Get fixed clusters
fixed_vec_bool     = zeros(1, par.max_clus);
new_fixed_vec_bool = zeros(1, par.max_clus);
for i=1:par.max_clus
    if (i < 4)
        fixed_vec_bool(i) = get(handles.(['fix', num2str(i), '_button']), ...
                    'value');
    else
        % Get fixed clusters from aux figures
        fixed_vec_bool(i) = par.(['fix', num2str(i)]);
    end
    if (fixed_vec_bool(i) == 1)
        nclusters = nclusters + 1;
        fix_class = USER_DATA{9 + i}';
        classes(find(classes==nclusters)) = 0;
        classes(fix_class) = nclusters;
        new_fixed_vec_bool(nclusters) = 1;
    end
end

% Defines classes
clustered = [];
cont=0;
for i=1:par.max_clus
    class_temp = find(classes==i);
    if ((length(class_temp) >= par.min_clus) | ((length(class_temp) > 0) & ...
                    (new_fixed_vec_bool(i) == 1)))
        cont=cont+1;
        s_class{cont + 1} = class_temp;         % s_class: spike class.
        clustered = [clustered, s_class{cont + 1}];

        % preserve `fix'ed status:
        if (i < 4)
            set(handles.(['fix', num2str(cont), '_button']), 'value', ...
                              new_fixed_vec_bool(i));
        else
            % set in aux:
            par.(['fix', num2str(cont)]) = new_fixed_vec_bool(i);
        end
        if (new_fixed_vec_bool(i) == 1)
            USER_DATA{9 + cont} = class_temp;
        else
            USER_DATA{9 + cont} = [];
        end
    end
end
nclusters = cont;
s_class{1} = setdiff( 1:num_spikes, clustered );   % class #0

% Redefines classes
classes = zeros(num_spikes,1);
for i = 1:nclusters+1
    if ~ (isempty(s_class{1}) & i==1)
        classes(s_class{i}) = i-1;
    end
end

% Saves new classes
USER_DATA{6} = classes;
% clear `fix'ed class info for higher (currently unused) classes:
for i=(9+cont+1):22
    USER_DATA{i} = [];
end
par = unfix_some(handles, par, (cont+1):13);
USER_DATA{1} = par;
set(handles.wave_clus_figure,'userdata',USER_DATA);

% Clear plots
for i=1:4                                               
    axes(handles.(['spikes' num2str(i-1)]));
    cla reset;
    axes(handles.(['isi' num2str(i-1)]));
    cla reset;
end    
axes(handles.features); cla; reset(gca)
axes(handles.projections); cla; reset(gca)

if (length(classes) > size(spikes, 1))
    keyboard
    error('length(classes) > size(spikes, 1):  This is a BUG!!!');
end

fixed_y = get(handles.fixed_y_range, 'Value');   % are the y limits fixed?
if (fixed_y == 0)
    s = spikes(find(classes ~= 0), :);      % use only classified spikes.
    tight_ylim = [min(s(:)), max(s(:))];
end
plot_all = get(handles.plot_all_button, 'Value'); 

% Plot clusters
ylimit = [];
colors = ['k' 'b' 'r' 'g' 'c' 'm' 'y' 'b' 'r' 'g' 'c' 'm' 'y' 'b'];
for i = 1:nclusters+1
    if (length(handles.par.timetotal) > 1)
        channel = USER_DATA{32};
        tt_ind = channel;
    else
        tt_ind = 1;
    end
    if ~ (isempty(s_class{1}) & i==1)
        %PLOTS SPIKES OR PROJECTIONS
        hold(handles.projections, 'on');
        if (plot_all == 1)
            max_spikes=min(length(s_class{i}),par.max_spikes);
            display_spikes = select_spikes_for_plot(spikes(s_class{i}, :), ...
                        max_spikes);
%            plot(handles.projections, spikes(s_class{i}(1:max_spikes),:)', ...
%                 colors(i));
            plot(handles.projections, display_spikes', colors(i));
        else
            av = mean(spikes(s_class{i},:));
            plot(handles.projections, 1:ls, av, 'color', colors(i), ...
                 'linewidth', 2);
        end
        xlim(handles.projections, [1 ls])

        hold(handles.features, 'on');
        plot(handles.features, inspk(s_class{i},1),inspk(s_class{i},2), ...
             ['.', colors(i)], 'markersize', .5);
        
        if i < 5
            h_spikes = handles.(['spikes' num2str(i-1)]);
            h_isi    = handles.(['isi' num2str(i-1)]);
            
            hold(h_spikes, 'on');
            av = mean(spikes(s_class{i},:));
            avup = av + par.to_plot_std * std(spikes(s_class{i},:));
            avdw = av - par.to_plot_std * std(spikes(s_class{i},:));
            if plot_all ==1
                plot(h_spikes, display_spikes', 'color', colors(i));
                if i==1
                    plot(h_spikes, 1:ls,av,'c', 'linewidth',2);
                    plot(h_spikes, 1:ls,avup,'c', 'linewidth',.5)
                    plot(h_spikes, 1:ls,avdw,'c', 'linewidth',.5)
                else
                    plot(h_spikes, 1:ls,av,'k', 'linewidth',2);
                    plot(h_spikes, 1:ls, avup, 1:ls, avdw, ...
                         'color', [.4 .4 .4], 'linewidth', .5)
                end
            else
                plot(h_spikes, 1:ls,av,'color', colors(i),'linewidth',2)
                plot(h_spikes, 1:ls,avup,1:ls,avdw, 'color', [.65 .65 .65], ...
                     'linewidth', .5)
            end
            xlim(h_spikes, [1 ls]);
            if (fixed_y == 0)
                if ((i == 1) & plot_all)
                    % unclassified spikes use a separate range:
                    spike_range = [min(spikes(:)), max(spikes(:))];
                    ylim(h_spikes, spike_range);
                    ylim(handles.projections, spike_range);
                elseif ((i == 1) & (~plot_all))
                    s0 = spikes(find(classes == 0), :); % only unclassified spks
                    ylim(h_spikes, [min(s0(:)), max(s0(:))]);
                else
                    switch (length(tight_ylim))
                     case 2
                      ylim(h_spikes, tight_ylim);
                     case 1
                      ylim(h_spikes, [tight_ylim, tight_ylim.*1.1]);
                     case 0
                      ylim(h_spikes, [0, 1]);
                     otherwise
                      error(sprintf('Unknown tight_ylim length (%d).\n', ...
                                  length(tight_ylim)));
                    end
                end
            end
            if i>1;
                if ((fixed_y == 1) | (plot_all == 0))
                    ylimit = [ylimit; ylim];
                else
                    ylimit = [ylimit; tight_ylim];
                end
            end
            
            % ARIEL: Modify, 02.11.2005:
            aux_num = length(s_class{i});
            
            % ARIEL: added SNR, 06.03.2016:
            SNR = cluster_SNR(spikes, s_class{i});
            title(h_spikes, ...
                  sprintf('Cluster %d:  # %d (%.2f%%)\n%.2fHz  SNR=%.1f', i-1, ...
                        aux_num, aux_num ./ num_spikes .* 100, ...
                        aux_num ./ handles.par.timetotal(tt_ind), SNR), ...
                  'Fontweight', 'bold');
            % ARIEL: 02.11.2005:
            set(h_spikes, 'XMinorTick', 'on', 'YMinorTick', 'on');
            
            times=diff(spk_times(s_class{i}));
            % ARIEL: Modified, 18.02.2007:
%            [N,X]=hist(times,0:par.(['bin_step', num2str(i-1)]):par.(['nbins' num2str(i-1)]));
%            bar(h_isi, X(1:end-1),N(1:end-1))
            hist_edges = 0:par.(['bin_step', num2str(i-1)]):par.(['nbins' num2str(i-1)]);
            if (~isempty(times))    % empty times happens for a 1 spike cluster.
                N = histc(times, hist_edges);
                X = hist_edges(1:(end-1)) + diff(hist_edges)./2;    % bin centers.
                h_bar = bar(h_isi, X, N(1:end-1));    % exclude last bin of N (=higher ISIs)
                set(h_bar, 'facecolor', colors(i), ...
                              'edgecolor', colors(i), 'linewidth', 0.01);
            else
                N = zeros(1, length(hist_edges));
            end
            xlim(h_isi, [0 par.(['nbins' num2str(i-1)])]);
            % ARIEL: Modified, 02.11.2005:
%            title(h_isi, sprintf('%d (%.2f%%)  in < 3ms', sum(N(1:3)), ...
%                        sum(N(1:3)) ./ aux_num .* 100));
            title(h_isi, sprintf('%d (%.2f%%)  in < 2ms', sum(N(1:2)), ...
                        sum(N(1:2)) ./ aux_num .* 100));
            xlabel(h_isi, 'ISI (ms)');
            % ARIEL: 02.11.2005:
            set(h_isi, 'TickDir', 'out');
            set(h_isi, 'XMinorTick', 'on');
        elseif i < 10 
            par.axes_nr = i;
            par.ylimit = ylimit;
            par.class_to_plot = s_class{i};
            par.plot_all_button = plot_all;
            USER_DATA{1} = par;
            set(handles.wave_clus_figure,'userdata',USER_DATA)
            wave_clus_aux0;
        else
            par.axes_nr = i;
            par.ylimit = ylimit;
            par.class_to_plot = s_class{i};
            par.plot_all_button = plot_all;
            USER_DATA{1} = par;
            set(handles.wave_clus_figure,'userdata',USER_DATA)
            wave_clus_aux1;
        end
    end
end

%Resize axis
if (~strcmp(char(handles.datatype),'Sc data') & ...
    ~strcmp(char(handles.datatype),'Sc data (pre-clustered)') & ...
    (fixed_y == 1))
    if (size(ylimit, 2) >= 2)
        ymin = min(ylimit(:,1));
        ymax = max(ylimit(:,2));
        for i=1:3
            ylim(handles.(['spikes', num2str(i)]), [ymin ymax]);
        end
    end
end

% raise main figure, to denote completion of plotting:
figure(h_fig);
drawnow;
