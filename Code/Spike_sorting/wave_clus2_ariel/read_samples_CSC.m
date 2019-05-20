function samples = read_samples_CSC(filename)
% read_samples_CSC    

% Author: Ariel Tankus.
% Created: 24.01.2005.

f=fopen(filename,'r');
fseek(f,16384+8+4+4+4,'bof'); % put pointer to the beginning of data

% LOAD CSC DATA
samples=fread(f,Inf,'512*int16=>int16',8+4+4+4);

fclose(f);
