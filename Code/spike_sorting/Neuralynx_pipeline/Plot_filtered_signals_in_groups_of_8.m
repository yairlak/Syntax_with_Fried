clear; close all; clc;

%%
patient = 'patient_482';
probes_names = {'rEC', 'rMH', 'RA', 'rSTGa', 'rAIP', 'rMC', 'rSTG', 'rIF', 'rSO', 'rSP', 'rOP', 'rIG', 'LMH', 'LP'}; % Patient 480
probes_names = {'lEC', 'laH', 'lA', 'lpHG', 'lSTG', 'lIP', 'lO', 'lIO', 'rEC', 'raH', 'rIO'}; % Patient 482


base_folder = ['/home/yl254115/Projects/single_unit_syntax/Data/UCLA/', patient];
% base_folder = ['/neurospin/unicog/protocols/intracranial/single_unit/Data/UCLA/', patient];
output_path = fullfile(base_folder,'ChannelsCSC');

% mkdir(output_path);
addpath(genpath('releaseDec2015'), genpath('NPMK-4.5.3.0'), genpath('functions'))


%% !!! sampling rate !!!! - make sure it's correct
sr = 30000; 
channels = 1:112;
not_neuroport = 1;

%%
cnt = 1; group = 1;
f = figure('visible', 'off', 'color', [1 1 1], 'units', 'normalized', 'position', [0 0 1 1]);
for channel = channels
%     fprtinf('Processing channel %i\n', channel)
    load(fullfile(output_path, ['Signal_filtered_', num2str(channel)]));
    ed = 100; % in sec
    yy = xf_detect(1:ed*sr);
    xx = (1:length(yy))/sr;
    subplot(8, 1, cnt)
    plot(xx, yy);
    if mod(channel-1,8) == 0
        title(sprintf('Probe location: %s', probes_names{group}))
    end
    line([0, ed],[thr, thr], 'color', 'g')
    line([0,ed],[-thr, -thr], 'color', 'g')
    line([0, ed],[thrmax, thrmax], 'color', 'r', 'linewidth', 5)
    line([0,ed],[-thrmax, -thrmax], 'color', 'r', 'linewidth', 5)
    xlim([0, ed])
    ylim([-150, 150])
    ylabel(sprintf('Ch %i', channel), 'fontsize', 12)
    cnt = cnt + 1;
    
    if mod(channel-1, 8) == 7
        xlabel('Time [sec]', 'fontsize', 16)
        fprintf('Saving figure for group %i...', group)
%         savefig(f, fullfile(output_path, ['Signal_filtered_in_eight_group_', num2str(group), '.fig']))
        saveas(f, fullfile(output_path, ['Signal_filtered_in_eight_group_', num2str(group), '.png']), 'png')
        close(f)
        fprintf('saved\n')
        f = figure('visible', 'off', 'color', [1 1 1], 'units', 'normalized', 'position', [0 0 1 1]);
        group = group + 1;
        cnt = 1;
    end
end