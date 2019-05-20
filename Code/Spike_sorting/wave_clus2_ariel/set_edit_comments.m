function set_edit_comments(comments)
% set_edit_comments    Set all user-editable comments.
%
%                      set_edit_comments(comments)
%                      comments - (max_classes+1)x1 - cell - cell array of
%                                          comments, one per class.
%
%                      See also: get_edit_comments, clear_edit_objs.

% Author: Ariel Tankus.
% Created: 13.06.2006.


for i=1:length(comments)
    edit_obj = findobj('Tag', sprintf('edit%d', i-1));
    set(edit_obj, 'String', comments{i});
end
