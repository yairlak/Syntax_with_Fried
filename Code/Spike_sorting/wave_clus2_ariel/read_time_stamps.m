function TimeStamps = read_time_stamps(filename)
% read_time_stamps    

% Author: Ariel Tankus.
% Created: 24.01.2005.

f=fopen(filename);
fseek(f,16384,'bof'); % Skip Header, put pointer to the first record

% Read all TimeStamps
TimeStamps=fread(f, Inf, 'int64', (4+4+4+2*512));

fclose(f);
