function rippletriggeredraster(channel,fcuts_high,fcuts_low,stdMult,evtDur)

%      ripple triggered raster plots
% 
% Input
% channel: e.g. 9
% fcuts - passband (e.g. [79 80 180 181]) for ripples
% stdMult - multiple of standard deviation used for event detection (e.g. 5)
% evtDur - minimum duration of an event in ms
% within this duration will be considered as a single event.
% e.g. 125 = 100msec for a signal   to 1250Hz 
% 
% Output
%
% all_events - all detected neural events
% spike_mat_ripple - rasters
% 
% the number of all_events may be less that spike_mat_ripples (for first
% and last event in the dataset)  if they happen very close to start or end
% of dataset
%
% Fanis Panagiotaropoulos June 2016



%load data





% filter   signal in the target band (e.g. ripple)
fsamp = 2000;
[filteredSignal_highfreq]= filterSignal( Signal,fcuts_high,fsamp);


% get low frequency signal 
[filteredSignal_lowfreq]= filterSignal( Signal,fcuts_low,fsamp);
% detect neural events in the target filtered signal (e.g. ripples)
evtTime=event_detection(filteredSignal_highfreq,stdMult,'stdgauss',evtDur*fsamp/1000);








%%%%%%%%%%%%%%%%%%%%%%%%% plot downsampled signal

subplot(2,2,1)
plot( Signal)

set(gca,'XTick',[0  size( Signal,1)] )
    set(gca,'XTickLabel',[0 size( Signal,1)/625] )
          axis([0   size( Signal,1)  min( Signal) max( Signal) ])

xlabel('seconds')
title(sprintf('  signal (.1-625Hz)'))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%%%%% get signals around event time
subplot(2,2,3)
for k=1:length(evtTime)
    try
highfreq_events(k,:)=filteredSignal_highfreq(evtTime(k)-fsamp:evtTime(k)+fsamp);
lowfreq_events(k,:)=filteredSignal_lowfreq(evtTime(k)-fsamp:evtTime(k)+fsamp); %get the low frequency signal around the target event times
dec_signal(k,:)= Signal(evtTime(k)-fsamp:evtTime(k)+fsamp);   
    end
end

plot(mean(zscore(highfreq_events'),2),'b','LineWidth',1)
hold on
plot(mean(zscore(lowfreq_events'),2),'r','LineWidth',2)
hold on
plot(mean(zscore(dec_signal'),2),'m','LineWidth',2)
hold on
onset = [626 626];
plot(onset,[-5 5],'--','color', [0.5 0.5 0.5],'LineWidth',0.2);

axis([626-626/2 626+626/2 min(mean(zscore(dec_signal'),2))-1 max(mean(zscore(highfreq_events'),2))+1]);
ylabel('z score')
xlabel('Time [ms]')
set(gca,'XTick',[626-626/2  626 626+626/2] )
    set(gca,'XTickLabel',[-500 0 500] ); 
    
    legend(sprintf ('80-180Hz') , sprintf ('1-4Hz'),sprintf ('.1-625Hz' )) 
        legend BOXOFF
    title(sprintf('Average Ripple triggered Sharp Wave'))





  

figure
%[tfmap, tfmapvar, freqs, timesout,phasemap] =morlettimefreq(dec_signal',625,'comptype','spectrogram','freqs',[10:250]);
[tfmap, tfmapvar, freqs, timesout,phasemap] =morlettimefreq(dec_signal',625,'comptype','spectrogram');
imagesc(mean(tfmap,3)');
 axis xy

set(gca,'XTick',[round(round(length(dec_signal)/2)-625*100/1000) round(length(dec_signal)/2) round(round(length(dec_signal)/2)+625*100/1000)])
set(gca,'XTickLabel',[-100 0 100] )
axis([round(round(length(dec_signal)/2)-625*100/1000) round(round(length(dec_signal)/2)+625*100/1000) 1 length(freqs)])
set(gca,'YTick',[1:25:length(freqs)] )
set(gca,'YTickLabel',[freqs(1:25:end)] )
xlabel('Time [ms]')
ylabel('Frequency [Hz]')



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

