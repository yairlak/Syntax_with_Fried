function behav = calc_behav_performance(key_was_pressed_after_sentence, settings)

for block = 1:length(key_was_pressed_after_sentence)
    curr_presses = key_was_pressed_after_sentence{block};
    behav.TP(block) = sum(ismember(curr_presses, settings.food_related_sentences));
    behav.FN(block) = sum(1-ismember(settings.food_related_sentences, curr_presses));
    behav.accuracy(block) = behav.TP(block)/length(settings.food_related_sentences);
end
behav.accuracy_all = mean(behav.accuracy);
end