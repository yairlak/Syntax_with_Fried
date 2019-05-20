function g = gauss(t, sigma, mu)
% GAUSSIAN	Return the value of a gaussian with mean `mu' and standard
%		deviation `sigma' at point(s) `t'.
%		
%		G = GAUSSIAN(T, SIGMA, MU)
%		T     - scalar/vector/matrix.  At each element, calculates the
%		           Gaussian.
%		SIGMA - Standard deviation of the Gaussian.
%		MU    - mean of the Gaussian.
%		
%		G     - value of the Gaussian at point(s) T.
%		

%
% Written by Ariel Tankus, 19.9.96.
%

if nargin < 3, mu = 0; end
if nargin < 2, sigma = 1; end

g = 1 / (sqrt(2*pi) * sigma) .* exp(-(t-mu) .^ 2 / (2*sigma^2));

% g = exp(-(t-mu) .^ 2 / (sigma^2));
