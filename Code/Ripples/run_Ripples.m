clear; close all; clc

%% Settings
hospital = 'UCLA';
patient = 'patient_479';
settings.path2data = fullfile('..','..','Data', hospital, patient, 'ChannelsCSC');
settings.path2output = fullfile('..', '..', 'Output');

%% Parameters
fsamp = 30000; % sampling frequency of the original signal [Hz] (e.g., 2000 [Hz])
fcuts_high  = [79 80 180 181]; % passband (e.g. [79 80 180 181]) for ripples
fcuts_low = [0 1 4 5]; % passband (e.g. [0 1 4 5]) for ripples
stdMult = 5; % multiple of standard deviation used for event detection (e.g. 5)
evtDur = 125; % minimum duration of an event in ms

%% Running over all channels
for channel = 1:1
    [highfreq_events, lowfreq_events, evtTime] = ...
        rippletriggeredSignal(channel,fcuts_high,fcuts_low,stdMult,evtDur, fsamp, settings); 
    

    curr_file_name = sprintf('highfreq_events_CSC%i.mat', channel);
    save(fullfile(settings.path2output, curr_file_name));
end
