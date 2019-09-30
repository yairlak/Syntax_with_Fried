# Patient 502 ch 57
python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_func "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"  

python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" 

python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len_gt_6_cont_complex "num_letters>6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

# Patient 502 ch 57

python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" 

python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_func "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"  

python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len_gt_6_cont_complex "num_letters>6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"


# Patient 505 ch 26
python plot_evoked_comparison_rasters.py -patient 505 -channel 26 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_func "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"  

python plot_evoked_comparison_rasters.py -patient 505 -channel 26 --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" 

python plot_evoked_comparison_rasters.py -patient 505 -channel 26 --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

python plot_evoked_comparison_rasters.py -patient 505 -channel 26 --queries-to-compare len_gt_6_cont_complex "num_letters>6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"


# Patient 505 ch 25 (micro)
python plot_evoked_comparison.py -patient 505 -channel 25 --micro-macro micro --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_func "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"  

python plot_evoked_comparison.py -patient 505 -channel 25 --micro-macro micro --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" 

python plot_evoked_comparison.py -patient 505 -channel 25 --micro-macro micro --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

python plot_evoked_comparison.py -patient 505 -channel 25 --micro-macro micro --queries-to-compare len_gt_6_cont_complex "num_letters>6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"


# Patient 502 ch 31
python plot_evoked_comparison_rasters.py -patient 502 -channel 31 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_func "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"  

python plot_evoked_comparison_rasters.py -patient 502 -channel 31 --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" 

python plot_evoked_comparison_rasters.py -patient 502 -channel 31 --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

python plot_evoked_comparison_rasters.py -patient 502 -channel 31 --queries-to-compare len_gt_6_cont_complex "num_letters>6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"


# Patient 479_11 ch 36
python plot_evoked_comparison_rasters.py -patient 479_11 -channel 36 --queries-to-compare len_3_4_5 "num_letters<6 and num_letters>2 and block in [1, 3, 5]" --queries-to-compare len_6_7_8 "num_letters<9 and num_letters>5 and block in [1, 3, 5]" --queries-to-compare len_9_10_11 "num_letters<12 and num_letters>8 and block in [1, 3, 5]" 


#python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2_func "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_cont_simple "num_letters==4 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len4_cont_complex "num_letters==4 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]" --queries-to-compare len4_func "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len6_cont_simple "num_letters==6 and word_type in ['content'] and morpheme_type==0 and block in [1, 3, 5]" --queries-to-compare len6_cont_complex "num_letters==6 and word_type in ['content'] and morpheme_type>0 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len4 "num_letters==4 and block in [1, 3, 5]" --queries-to-compare len6 "num_letters==6 and block in [1, 3, 5]" --queries-to-compare len8 "num_letters==8 and block in [1, 3, 5]" --queries-to-compare len10 "num_letters==10 and block in [1, 3, 5]"


#python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len2 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len4 "num_letters==4 and block in [1, 3, 5]" --queries-to-compare len6 "num_letters==6 and block in [1, 3, 5]" --queries-to-compare len8 "num_letters==8 and block in [1, 3, 5]" --queries-to-compare len10 "num_letters==10 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len4 "num_letters==4 and block in [1, 3, 5]" --queries-to-compare len6 "num_letters==6 and block in [1, 3, 5]" --queries-to-compare len8 "num_letters==8 and block in [1, 3, 5]" --queries-to-compare len10 "num_letters==10 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len2 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len3 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len4 "num_letters==4 and block in [1, 3, 5]" --queries-to-compare len5 "num_letters==5 and block in [1, 3, 5]" --queries-to-compare len6 "num_letters==6 and block in [1, 3, 5]" --queries-to-compare len7 "num_letters==7 and block in [1, 3, 5]" --queries-to-compare len8 "num_letters==8 and block in [1, 3, 5]" --queries-to-compare len9 "num_letters==9 and block in [1, 3, 5]" --queries-to-compare len10 "num_letters==10 and block in [1, 3, 5]" --queries-to-compare len11 "num_letters==11 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len3 "num_letters==2 and block in [1, 3, 5]" --queries-to-compare len4 "num_letters==4 and block in [1, 3, 5]" --queries-to-compare len5 "num_letters==5 and block in [1, 3, 5]" --queries-to-compare len6 "num_letters==6 and block in [1, 3, 5]" --queries-to-compare len7 "num_letters==7 and block in [1, 3, 5]" --queries-to-compare len8 "num_letters==8 and block in [1, 3, 5]" --queries-to-compare len9 "num_letters==9 and block in [1, 3, 5]" --queries-to-compare len10 "num_letters==10 and block in [1, 3, 5]" --queries-to-compare len11 "num_letters==11 and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 57 --queries-to-compare len2_con "num_letters==2 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len3_con "num_letters==3 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len4_con "num_letters==4 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len2_fun "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_fun "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_fun "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"

#python plot_evoked_comparison_rasters.py -patient 502 -channel 60 --queries-to-compare len2_con "num_letters==2 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len3_con "num_letters==3 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len4_con "num_letters==4 and word_type in ['content'] and block in [1, 3, 5]" --queries-to-compare len2_fun "num_letters==2 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len3_fun "num_letters==3 and word_type in ['function'] and block in [1, 3, 5]" --queries-to-compare len4_fun "num_letters==4 and word_type in ['function'] and block in [1, 3, 5]"
