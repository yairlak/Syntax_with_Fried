
total_events = [1: size(highfreq_events,1)];
for ripple = 1:length(total_events)
  f1 = figure('visible','off','color',[1 1 1]);
  plot(highfreq_events(ripple,:));
  xlim([-1000 5000])
  xlabel('Time (in samples)')
  ylabel('Amplitude (mV)'); hold on;
  plot(get(gca,'xlim'),[0 0],'k--'); hold on;
  plot([0 0],get(gca,'ylim'),'r-'); hold on
  plot([4000 4000],get(gca,'ylim'),'r-'); hold on
  title({'Ripple n' num2str(total_events(ripple)), 'observed in electrode n 158 of patient TS096'})
  file_name = sprintf('figure_%i.png', ripple);
  saveas(f1, fullfile('C:\Users\Lenovo\Dropbox\lfpcodes\Figures', file_name), 'png')
end

