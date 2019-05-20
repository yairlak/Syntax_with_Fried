clear all; close all; clc
files = dir('*.wav');

for f = 1:length(files)
    curr_fn = files(f).name;
    [y, fs] = audioread(curr_fn);
%     y_norm = y/(10*max(abs(y)));
    y_norm = 1e-2*y/rms(y);
    audiowrite(fullfile('normalized', curr_fn), y_norm, fs)
end
