function scaled = scl(im, low, high)
% SCL	Scale the image `im' to the range: [low,high].  The default range is:
%	[0,255].
%
%       scaled = scl(im, low, high)
%       im   - array of doubles - image.
%       low  - 1x1 - lowest value.
%       high - 1x1 - highest value.

% Author: Ariel Tankus.
% Created: 19.9.96.
% Modified: 18.3.2000. (doc improvement).
% Modified: 29.4.2007. Avoid usage of min2, max2, to allow multi-dimensional
%                      arrays too.
% Modified: 10.07.2007.  Ignore NaN values: max,min |--> nanmax,nanmin.


if nargin < 2 
    low = 0;
    high = 255;
end

vec_im = im(:);
non_nan_vec_im = ((~isinf(vec_im)) & (~isnan(vec_im)));
M = nanmax(im(non_nan_vec_im));
m = nanmin(im(non_nan_vec_im));

scaled = (im - m)./ (M - m) * (high - low) + low;
