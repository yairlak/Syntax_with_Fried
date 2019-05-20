function [] = clus_manip_print_all(ch_list)
% clus_manip_print_all    

% Author: Ariel Tankus.
% Created: 13.05.2018.


num_ch = length(ch_list);

for i=1:num_ch
    close all;
    clus_manip(i);
    % -r0: screen resolution.
    set(4, 'Position', [1 34 1600 747]);
    set(gcf, 'PaperType', 'A4');
%    set(4, 'PaperOrientation', 'Portrait');
    set(4, 'PaperOrientation', 'Landscape');
%    set(gcf, 'PaperPosition', [0.25 0.25 21.0000-0.5 29.7000-0.5]);
    set(gcf, 'PaperPositionMode', 'auto');
    print(4, '-dpng', '-r0', sprintf('clus_manip%d.png', i));
end
