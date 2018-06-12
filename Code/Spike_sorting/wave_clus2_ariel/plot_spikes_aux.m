function plot_spikes_aux(handles, aux_num)
% ARIEL: 29.11.2005: aux_num - number of auxiliary figure opened.
%                              0-the first; 1-the second; etc. 
USER_DATA = get(handles.(['wave_clus_aux', num2str(aux_num)]),'userdata');
par = USER_DATA{1};
spikes = USER_DATA{2};
spk_times = USER_DATA{3};
inspk = USER_DATA{7};
[num_spikes, ls] = size(spikes);
par.to_plot_std = 1;                % # of std from mean to plot
axes_nr = par.axes_nr;
ylimit = par.ylimit;
class_to_plot = par.class_to_plot;
max_spikes = min(par.max_spikes, length(class_to_plot));


% Plot clusters
colors = ['k' 'b' 'r' 'g' 'c' 'm' 'y' 'b' 'r' 'g' 'c' 'm' 'y' 'b'];
axes(handles.(['spikes', num2str(axes_nr-1)]));
cla reset
hold on
av   = mean(spikes(class_to_plot,:));
avup = av + par.to_plot_std * std(spikes(class_to_plot,:));
avdw = av - par.to_plot_std * std(spikes(class_to_plot,:));
if par.plot_all_button ==1
    plot(spikes(class_to_plot(1:max_spikes),:)','color',colors(axes_nr));
    plot(1:ls,av,'k','linewidth',2);
    plot(1:ls,avup,1:ls,avdw,'color',[.4 .4 .4],'linewidth',.5)
else
    plot(1:ls,av,'color',colors(axes_nr),'linewidth',2)
    plot(1:ls,avup,1:ls,avdw,'color',[.65 .65 .65],'linewidth',.5)
end
xlim([1 ls])
sz_cur_class = length(class_to_plot);
if (length(par.timetotal) > 1)
    channel = USER_DATA{32};
    tt_ind = channel;
else
    tt_ind = 1;
end

% ARIEL: added SNR, 06.03.2016:
SNR = cluster_SNR(spikes, class_to_plot); 
title(sprintf('Cluster %d:  # %d (%.2f%%)\n%.2fHz  SNR=%.1f', axes_nr-1, sz_cur_class, ...
              sz_cur_class./num_spikes .* 100, sz_cur_class./par.timetotal(tt_ind), SNR), ...
      'Fontweight', 'bold');

axes(handles.(['isi', num2str(axes_nr-1)]));
times = diff(spk_times(class_to_plot));
% ARIEL: Modified, 18.02.2007:
%[N,X]=hist(times,0:par.(['bin_step', num2str(axes_nr-1)]):par.(['nbins', num2str(axes_nr-1)]));
%bar(X(1:end-1),N(1:end-1))
hist_edges = 0:par.(['bin_step', num2str(axes_nr-1)]):par.(['nbins' num2str(axes_nr-1)]);
if (~isempty(times))    % empty times happens for a 1 spike cluster.
    N = histc(times, hist_edges);
    X = hist_edges(1:(end-1)) + diff(hist_edges)./2;    % bin centers.
    h_bar = bar(X, N(1:end-1));                      % exclude last bin of N (=higher ISIs)
    set(h_bar, 'facecolor', colors(axes_nr), ...
                  'edgecolor', colors(axes_nr), ...
                  'linewidth', 0.01);
else
    N = zeros(1, length(hist_edges));
end
xlim([0 par.(['nbins', num2str(axes_nr-1)])]);
%title(sprintf('%d (%.2f%%)  in < 3ms', sum(N(1:3)), ...
%            sum(N(1:3)) ./ sz_cur_class .* 100));
title(sprintf('%d (%.2f%%)  in < 2ms', sum(N(1:2)), ...
            sum(N(1:2)) ./ sz_cur_class .* 100));
xlabel('ISI (ms)');

%Resize axis
ymin = min(ylimit(:,1));
ymax = max(ylimit(:,2));
%axes(handles.([spikes, num2str(axes_nr-1)]));
%ylim([ymin ymax]);
axes(handles.(['spikes', num2str(axes_nr-1)]));
ylim([ymin ymax]);

%for i=1:5
%    set(handles.(['fix', num2str(i+3+5*aux_num), '_button']),'value',0);
%end
