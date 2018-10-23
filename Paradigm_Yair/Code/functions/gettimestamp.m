function timestamp = gettimestamp()
    formatOut = 'yyyymmmdd_hhMMss';
    timestamp = datestr(datetime('now'), formatOut);
end