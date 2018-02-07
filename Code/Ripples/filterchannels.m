
function filterchannels

channels = [1:24 33:56];
emptychannels=[25:32];
analog_channel=129;
fcuts_high=[79 80 180 181];
fcuts_low=[10 11 20 21];
fsamp = 2000;



parfor channel=1:length(channels) 
    disp(channel)
filteredSignal_highfreq{channel}= filterdecimatedSignal(decimatedSignal{channel},fcuts_high,fsamp);
filteredSignal_lowfreq{channel}= filterdecimatedSignal(decimatedSignal{channel},fcuts_low,fsamp);
end


neural.highpassfiltered=filteredSignal_highfreq;
neural.lowpassfiltered=filteredSignal_lowfreq;
neural.fsamp=fsamp;
neural.highpass=fcuts_high;
 save neural neural -v7.3


