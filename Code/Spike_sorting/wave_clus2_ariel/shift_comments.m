function shift_comments(shift_from, max_classes)
% shift_comments    Shift comments by one.  Copy the contents of the comment
%                   strings starting at a given edit object to the previous
%                   edit object.  This is necessary when a class is rejected,
%                   and all comments shift.
%
%                   shift_comments(shift_from, max_classes)
%                   max_classes - 1x1 - number of classes to consider.
%                   shift_from  - 1x1 - index of edit object to start the
%                                       shift from.  The comment of this
%                                       object will move to the previous
%                                       one.  Note, that this is the first
%                                       object to move, NOT the one being
%                                       rejected.
%
%                      See also: clear_edit_objs.

% Author: Ariel Tankus.
% Created: 03.02.2006.


prev_edit_obj = findobj('Tag', sprintf('edit%d', shift_from-1));
for i=shift_from:max_classes
    edit_obj = findobj('Tag', sprintf('edit%d', i));
    set(edit_obj, 'String', get(prev_edit_obj, 'String'));
end
