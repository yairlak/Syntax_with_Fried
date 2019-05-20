clear all; close all; clc
%%
files = dir('*.wav');
for f = 1:length(files)
    curr_fn = files(f).name;
    [y, fs] = audioread(curr_fn);
    f = figure('color', [1 1 1], 'visible', 'off');
    plot(y)
    xlabel('Time', 'fontsize', 14)
    
    saveas(gcf,fullfile('..', 'Figures', [curr_fn(1:end-4), '.png']), 'png')
end
