clear all; close all; clc
%%
files = dir('*.wav');
for f = 1:length(files)
    curr_fn = files(f).name;
    [y, fs] = audioread(curr_fn);
    file_lens(f) = length(y)/fs * 1000;
end
f = figure('color', [1 1 1]);
hist(file_lens)
xlabel('Stimulus length [ms]', 'fontsize', 14)
title(sprintf('Mean %1.2f std %1.2f', mean(file_lens), std(file_lens)), 'fontsize', 14);
saveas(gcf, ['file_lengths.png'], 'png')