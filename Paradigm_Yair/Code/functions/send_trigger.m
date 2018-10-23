function send_trigger(sio, dio, params, events, event_name, wait_secs)

if triggers && strcmp(params.location,'TLVMC') % Setup for ICHILOV Tel-Aviv
      fwrite(sio,events.(event_name)); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(wait_secs);
elseif triggers && strcmp(params.location,'UCLA') % Setup for UCLA
     DaqDOut(dio,params.portA,events.(event_name)); % send eventX TTL (0-255)
     WaitSecs(events.ttlwait);
     DaqDOut(dio,params.portA,events.eventreset); % reset Daq interface
     WaitSecs(wait_secs);
end

end