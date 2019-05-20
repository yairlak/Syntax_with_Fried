function USER_DATA = fix_some(handles, USER_DATA, classes, fix_inds, val)
% fix_all    Make some clusters fixed or unfixed.  Also updates the USER_DATA
%            (unlike unfix_some, unfix_all).
%
%            USER_DATA = fix_some(handles, USER_DATA, classes, fix_inds, val)
%
%              See also:  unfix_some, unfix_all, get_fixed_vec, set_fixed_vec,
%                         shift_fixed_buttons.

% Author: Ariel Tankus.
% Created: 03.07.2006.


par = USER_DATA{1};

% clear all clusters `fix'ed state:
for i=fix_inds
    if (i < 4)
        set(handles.(['fix' num2str(i) '_button']), 'value', val);
    else
        par.(['fix', num2str(i)]) = val;
    end
    USER_DATA{9+i} = find(classes == i);
end

USER_DATA{1} = par;
