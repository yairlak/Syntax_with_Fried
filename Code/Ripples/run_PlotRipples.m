clear; close all; clc

%%
settings.path2Ripples = fullfile('..', '..', 'Output');
settings.path2output = fullfile('..', '..', 'Figures', 'Ripples');

%%
for channel = 9:16
    
    curr_file_name = sprintf('highfreq_events_CSC%i.mat', channel);
    load(fullfile(settings.path2Ripples, curr_file_name), 'highfreq_events');

    total_events = [1: size(highfreq_events,1)];
    for ripple = 1:length(total_events)
      fprintf('Channel %i, Ripple %i\n', channel, ripple)
      f1 = figure('visible','off','color',[1 1 1]);
      plot(highfreq_events(ripple,:));
      xlim([0 6000])
      xlabel('Time (in samples)')
      ylabel('Amplitude (mV)'); hold on;
      plot(get(gca,'xlim'),[0 0],'k--'); hold on;
%       plot([0 0],get(gca,'ylim'),'r-'); hold on
%       plot([4000 4000],get(gca,'ylim'),'r-'); hold on
      
      title_str = sprintf('Ripple %i, channel %i', ripple, channel);
      title(title_str)
      file_name = sprintf('channel_%i_ripple_%i.png', channel, ripple);
      saveas(f1, fullfile(settings.path2output, file_name), 'png')
    end
end