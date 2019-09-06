#for CH in 25 26 27 28 29 30 31 32 57 58 59 60 61 62 63 64;
#do
#    python plot_evoked_comparison.py -patient 505 -channel $CH --queries-to-compare "Short words" "word_position==2 and num_letters<5 and block in [1, 3, 5]" --queries-to-compare "Intermediate" "word_position==2 and (num_letters>=5 and num_letters<8) and block in [1, 3, 5]" --queries-to-compare "Long words" "word_position==2 and (num_letters>=8 and num_letters<11) and block in [1, 3, 5]"

#done


for CH in 17 18 19 20 21 22 23 24;
do
    python plot_evoked_comparison.py -patient 505 -channel $CH --queries-to-compare "A_He" "word_position==1 and word_string=='he' and block in [2, 4, 6]" --queries-to-compare "A_She" "word_position==1 and word_string=='she' and block in [2, 4, 6]"
    python plot_evoked_comparison.py -patient 505 -channel $CH --queries-to-compare "V_He" "word_position==1 and word_string=='he' and block in [1, 3, 5]" --queries-to-compare "V_She" "word_position==1 and word_string=='she' and block in [1, 3, 5]"

done
