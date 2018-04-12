function evtTime=event_detection(Sig, stdMult,estimType,evtDur)
%EVENT_DETECTION - event detection based on the time course of filtered signal
%evtTime=EVENT_DETECTION(Sig, stdMult,estimType,evtDur)
%
%  inputs
%
%	Sig - 1-D signal
%
%	stdMult - multiple of the standard deviation used for detection 
%
%	estimType - type of estimation of standard deviation :
%       'stdgauss': simple estimator of standard deviation
%       'madgauss': robust estimator of standard deviation based on median
%       absolute deviation
%
%	evtDur - minimum duration of an event in number of samples, detections
%	within this duration will be considered as a single event.
%
%
%  outputs
%
%	evtTime - integer vector indicating the time samples where events are
%	detected.
%
%
% Author : Michel Besserve, MPI for Intelligent Systems, MPI for Biological Cybernetics, Tuebingen, GERMANY
if nargin<3
    estimType='stdgauss';
end
if nargin<4
    evtDur=1;
end


[evtDetect]=sigDetectThres(Sig,estimType,stdMult);
evtClust = conncomp1d(filtfilt(hanning(evtDur)/sum(hanning(evtDur)),1,double(evtDetect)));
if evtClust.NumObjects==0, evtTime=[];return,end
for ktime=1:length(evtClust.PixelIdxList)
   [maxH(ktime),tmpTime]=max(abs(Sig(evtClust.PixelIdxList{ktime})));
   evtTime(ktime)=evtClust.PixelIdxList{ktime}(tmpTime);
end
