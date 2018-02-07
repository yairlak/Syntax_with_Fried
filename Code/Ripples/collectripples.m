function [prescr_events_per_sec,text_events_per_sec,context_events_per_sec,recallcue_events_per_sec,recall_events_per_sec,postscr_events_per_sec]=collectripples(channels)

%channels = [97:128];
for i=channels(1:end)
    try
[prescr_events_per_sec{i},text_events_per_sec{i},context_events_per_sec{i},recallcue_events_per_sec{i},recall_events_per_sec{i},postscr_events_per_sec{i}]=rippletriggeredraster(i,[75 80 180 185],[0 1 4 5],5,100);
    end
end

figure
%bar([mean(cat(2,text_events_per_sec{:})),mean(cat(2,context_events_per_sec{:})),mean(cat(2,recallcue_events_per_sec{:})),mean(cat(2,recall_events_per_sec{:}))])

 m=[mean(cat(2,prescr_events_per_sec{:})),mean(cat(2,text_events_per_sec{:})),mean(cat(2,context_events_per_sec{:})),mean(cat(2,recallcue_events_per_sec{:})),mean(cat(2,recall_events_per_sec{:})),mean(cat(2,postscr_events_per_sec{:}))];
 n=[std(cat(2,prescr_events_per_sec{:}))/sqrt(length(cat(2,prescr_events_per_sec{:}))),std(cat(2,text_events_per_sec{:}))/sqrt(length(cat(2,text_events_per_sec{:}))),std(cat(2,context_events_per_sec{:}))/sqrt(length(cat(2,context_events_per_sec{:}))),std(cat(2,recallcue_events_per_sec{:}))/sqrt(length(cat(2,recallcue_events_per_sec{:}))),std(cat(2,recall_events_per_sec{:}))/sqrt(length(cat(2,recall_events_per_sec{:}))),std(cat(2,postscr_events_per_sec{:}))/sqrt(length(cat(2,postscr_events_per_sec{:})))];
 bar(m)
 hold on
 errorbar(m,n,'LineStyle','none','LineWidth',2,'Color',[0 0 0])
 
set(gca,'xtick',[1 2 3 4 5 6],'xticklabel',{'prescreening','text','encoding','recall cue','recall','postscreening'},'FontWeight', 'bold','fontsize',7);
ylabel('events/sec')


saveas(gcf,sprintf (['average ripples' ]),'fig')