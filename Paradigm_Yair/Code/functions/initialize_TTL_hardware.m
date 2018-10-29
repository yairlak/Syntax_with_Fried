function [sio, dio, DaqDOut, hwline, laststim] = initialize_TTL_hardware(triggers, params, events)
sio=[]; dio=[]; DaqDOut=[]; hwline=[]; laststim=[];

if triggers && strcmp(params.location,'TLVMC')
    sio = serial(params.sio,'BaudRate',115200,'Terminator', []);
    fopen(sio);     %remember to close manually if you terminal execution early
    fwrite(sio,1); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.5);
    fwrite(sio,2); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.5);
    fwrite(sio,3); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.5);
    fwrite(sio,4); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset);
end

if triggers && strcmp(location,'TLVMC') % mark the beginning of the experiment with four 255 triggers separated 100ms from each other
    fwrite(sio,events.event255); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.1);
    fwrite(sio,events.event255); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.1);
    fwrite(sio,events.event255); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(0.1);
    fwrite(sio,events.event255); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset);
end

% Initialize DAQ
if triggers && strcmp(params.location,'UCLA')
    dio=DaqDeviceIndex;                                     	            % get a handle for the USB-1208FS
    hwline=DaqDConfigPort(dio,0,0);                                         % configure digital port A for output
    DaqDOut(dio,params.portA,events.eventreset);
    hwline=DaqDConfigPort(dio,1,0);                          	            % configure digital port B for output
    DaqDOut(dio,params.portB,events.eventreset); 
    laststim = 0;
end