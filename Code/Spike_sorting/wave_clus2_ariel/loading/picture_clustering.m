function [] = picture_clustering(ch_list, use_print_cmd)
% produce_clustering_images    

% Author: Ariel Tankus.
% Created: 27.07.2006.

if (nargin < 2)
    use_print_cmd = false;
end

if (nargin < 1)
    ch_list = 1:64;
end

for ch=ch_list

    t = tic;

    [h, h_feat] = clus_manip(ch);
    drawnow;
    for i=1:length(h)
        
        if (~use_print_cmd)
            frm = getframe(h(i));
            imwrite(frm.cdata, sprintf('fig2print_ch%d%c.png',ch,96+i), 'png');
                                    % ASCII for 'a', 'b', 'c', etc.
        else
            figure(h(i));
            print(h(i), '-dpng', ...
                  sprintf('fig2print_ch%d%c.png', ch, 96+i));
                                    % ASCII for 'a', 'b', 'c', etc.
        end
        close(h(i));
    end
    for i=1:length(h_feat)
        if (~use_print_cmd)
            frm = getframe(h_feat(i));
            imwrite(frm.cdata, sprintf('fig2print_ch%d_feat%c.png', ch, 96+i), 'png');
                                            % ASCII for 'a', 'b', 'c', etc.
        else
            figure(h_feat(i));
            print(h_feat(i), '-dpng', ...
                  sprintf('fig2print_ch%d_feat%c.png', ch, 96+i));
                                            % ASCII for 'a', 'b', 'c', etc.
        end
        close(h_feat(i));
    end
    
    toc(t);
end
