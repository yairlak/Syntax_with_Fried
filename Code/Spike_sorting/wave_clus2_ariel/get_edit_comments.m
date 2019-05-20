function comments = get_edit_comments(max_classes)
% get_edit_comments    Get all comments edited by the user.
%
%                      comments = get_edit_comments(max_classes)
%                      max_classes - 1x1 - number of classes to consider.
%                      comments - (max_classes+1)x1 - cell - cell array of
%                                          comments, one per class.
%
%                      See also: set_edit_comments, clear_edit_objs.

% Author: Ariel Tankus.
% Created: 03.02.2006.


comments = cell(max_classes+1, 1);
for i=0:max_classes
    edit_obj = findobj('Tag', sprintf('edit%d', i));
    comments{i+1} = get(edit_obj, 'String');
end
