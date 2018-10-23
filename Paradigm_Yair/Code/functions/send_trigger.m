function send_trigger(sio, dio, params, events, event_name, wait_secs)


if triggers && strcmp(location,'TLVMC') % mark the beginning of a new block with four 255 triggers separated 200ms from each other
      fwrite(sio,events.(event_name)); WaitSecs(events.ttlwait); fwrite(sio,events.eventreset); WaitSecs(wait_secs);
elseif triggers && strcmp(params.location,'UCLA') % mark the beginning of the experiment with four 255 triggers separated 100ms from each other
     DaqDOut(dio,params.portA,events.(event_name)); % send ?eventX' TTL (0-255)
     WaitSecs(events.ttlwait);
     DaqDOut(dio,params.portA,events.eventreset); % reset Daq interface
     WaitSecs(wait_secs);
end

end