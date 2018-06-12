function USER_DATA = shift_fixed_buttons(button_num, handles, USER_DATA, ...
            classes)
% shift_fixed_buttons    Following a rejection of a cluster, shift the
%                        `fix'ed values of all higher-numbered clustered by
%                        one.
%
%                        See also:  plot_spikes.

% Author: Ariel Tankus.
% Created: 12.06.2006.


par = USER_DATA{1};
counter = button_num;
for i=(button_num+1):13
    if (length(find(classes == i, 1)) > 0)
        % non-empty cluster
        USER_DATA{9+counter} = USER_DATA{9+i};
        if (i < 4)
            new_state = get(handles.(['fix', num2str(i), '_button']), 'value');
        else
            new_state = par.(['fix', num2str(i)]);   % from aux
        end

        if (counter < 4)
            set(handles.(['fix', num2str(counter), '_button']), 'value', ...
                              new_state);
        else
            % set in aux:
            par.(['fix', num2str(counter)]) = new_state;
        end
        counter = counter + 1;
    end
end

% un-fix clusters after the last:
for j=(counter+1):13
    USER_DATA{9+j} = [];
    if (j < 4)
        set(handles.(['fix', num2str(j), '_button']), 'value', 0);
    else
        % set in aux:
        par.(['fix', num2str(j)]) = 0;
    end
end

USER_DATA{1} = par;
