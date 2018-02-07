function [highfreq_events, lowfreq_events, evtTime]=rippletriggeredSignal(channel,fcuts_high,fcuts_low,stdMult,evtDur, fsamp, settings)

%%      ripple triggered raster plots
% 
% Input
% channel: e.g. 9
% fcuts - passband (e.g. [79 80 180 181]) for ripples
% stdMult - multiple of standard deviation used for event detection (e.g. 5)
% evtDur - minimum duration of an event in ms
% fsamp - sampling frequency of the original signal [Hz] (e.g., 2000 [Hz])
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

% ------------------------------------------------------
% Together with Extract_Events.m these scripts allow for detecting
% ripples in different regions of interest  and specified time windows
% --------------------------------------------------------

%% 
%% Load data
Channel_file_name = sprintf('CSC%i.mat', channel);
data = load(fullfile(settings.path2data, Channel_file_name));
Signal = im2double(data.data);
Signal = Signal';

%% Analyzing the data
n = 10;
sprintf('Downsampling...')
Signal = decimate(Signal, n); % Downsample by a factor of 10 (from 30 to 3kHz)
% Update freq sampling
fsamp = fsamp/n;

sprintf('Filtering...\n')
[filteredSignal_highfreq]= filterSignal(Signal,fcuts_high,fsamp);
% get low frequency signal 
sprintf('Get low frequency signal...\n')
[filteredSignal_lowfreq]= filterSignal( Signal,fcuts_low,fsamp);
% detect neural events in the target filtered signal (e.g. ripples)
sprintf('Detect neural events...\n')
evtTime=event_detection(filteredSignal_highfreq,stdMult,'stdgauss',evtDur*fsamp/1000);

%% Plot downsampled signal
% subplot(2,2,1)
% plot( Signal)
% 
% set(gca,'XTick',[0  size( Signal,1)] )
%     set(gca,'XTickLabel',[0 size( Signal,1)/625] )
%           axis([0   size( Signal,1)  min( Signal) max( Signal) ])
% 
% xlabel('seconds')
% title(sprintf('  signal (.1-625Hz)'))
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% %% Get signals around event time
% subplot(2,2,3)
for k=1:length(evtTime)
    try
        highfreq_events(k,:)=filteredSignal_highfreq(evtTime(k)-fsamp:evtTime(k)+fsamp);
        lowfreq_events(k,:)=filteredSignal_lowfreq(evtTime(k)-fsamp:evtTime(k)+fsamp); %get the low frequency signal around the target event times
        dec_signal(k,:)= Signal(evtTime(k)-fsamp:evtTime(k)+fsamp);   %changed from Signal to dec_signal
    end
end
% 
% plot(mean(zscore(highfreq_events'),2),'b','LineWidth',1)
% hold on
% plot(mean(zscore(lowfreq_events'),2),'r','LineWidth',2)
% hold on
% plot(mean(zscore(dec_signal'),2),'m','LineWidth',2)
% hold on
% onset = [1000 1000];
% plot(onset,[-2 2],'--','color', [0.5 0.5 0.5],'LineWidth',0.2);
% 
% axis([626-626/2 626+626/2 min(mean(zscore(dec_signal'),2))-1 max(mean(zscore(highfreq_events'),2))+1]);
% ylabel('z score')
% xlabel('Time [ms]')
% set(gca,'XTick',[626-626/2  626 626+626/2] )
% set(gca,'XTickLabel',[-500 0 500] ); 
%     
% legend(sprintf ('80-180Hz') , sprintf ('1-4Hz'))  % ,sprintf ('.1-625Hz' )
% legend BOXOFF
% title(sprintf('Average Ripple triggered Sharp Wave'))
end
