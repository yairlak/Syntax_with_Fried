function display_file_name(pathname, filename, handles)
% display_file_name    

% Author: Ariel Tankus.
% Created: 04.12.2005.


min_len_path = 30;

if (length(pathname) <= min_len_path)
    set(handles.file_name,'string',[pathname filename]);
else
    set(handles.file_name, 'string', ...
                      ['...', pathname((end-min_len_path+4):end), filename]);
end
