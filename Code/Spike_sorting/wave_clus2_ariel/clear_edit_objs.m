function [] = clear_edit_objs()
% clear_edit_objs    Clear all comments.
%
%                    clear_edit_objs
%
%                    See also: get_edit_comments.

% Author: Ariel Tankus.
% Created: 03.02.2006.


num_edit_objs = 13;

for i=0:num_edit_objs
    edit_obj = findobj('Tag', sprintf('edit%d', i-1));
    if (~isempty(edit_obj))
        set(edit_obj, 'String', '');
    end
end
