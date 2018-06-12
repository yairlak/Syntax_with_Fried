function par = unfix_all(handles, par)
% unfix_all    Make all clusters not fixed.
%
%              unfix_all(handles, par)
%
%              See also:  get_fixed_vec, shift_fixed_buttons.

% Author: Ariel Tankus.
% Created: 13.06.2006.


% clear all clusters `fix'ed state:
for i=1:3
    set(handles.(['fix' num2str(i) '_button']), 'value', 0);
end
for i=4:13
    par.(['fix', num2str(i)]) = 0;
end
