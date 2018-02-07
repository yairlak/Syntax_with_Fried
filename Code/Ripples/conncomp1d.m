function [cc,y]=conncomp1d(x)
%CONNCOMP1D - extracts connected components from a 1d signal
%[cc,y]=CONNCOMP1D(x)
%
%  inputs
%
%	x - logical input
%
%
%  outputs
%
%	cc - structure containing component information (.NumObjects: number of
%	components, .PixelIdxList:cell array containing indices of each
%	component)
%
%	y - state vector containg the compent idx corresponding to each input 
%	point
%
%
% Author : Michel Besserve, MPI for Intelligent Systems, MPI for Biological Cybernetics, Tuebingen, GERMANY
% 

siz_x=size(x);
if any(siz_x(2:end)>1)
    error('function only deals with column vector input')
end

x=x~=0;
if any(isnan(x))
    error('input contains nans')
end

state=0;
kcomp=0;
y=0*x;
for ktime=1:size(x,1)
    switch state
        case 0
       if x(ktime),state=1;kcomp=kcomp+1;end
        case 1
            if ~x(ktime),state=0;end
    end            
    y(ktime)=state*kcomp;
end

for kcomp=1:max(y)
    cc.PixelIdxList{kcomp}=find(y==kcomp);
end
cc.NumObjects=max(y);





