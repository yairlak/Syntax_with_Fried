nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_487 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_493 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_487 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_493 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_505 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &


nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "last_word==1 and Declarative==0 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_last_word_question_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [1, 3, 5]" --train-queries "word_string=='she' and block in [1, 3, 5]" > Logs_GAT/gat_he_she_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [1, 3, 5]" --train-queries "word_string=='they' and block in [1, 3, 5]" > Logs_GAT/gat_he_they_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='they' and block in [2, 4, 6]" > Logs_GAT/gat_he_they_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &


nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_487 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_493 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='they' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='boys' and block in [2, 4, 6]" > Logs_GAT/gat_he_they_boy_boys_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "Question_type_subject_object==1 and block in [1, 3, 5] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [1, 3, 5] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &



nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_505 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &


nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_482 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_487 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_493 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_505 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &


# 502
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_502 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &




# 479, 482, 505
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &


# 479, 482, 502, 505
nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_word_end_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_word_end_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_string.str.len()==2 and block in [1, 3, 5]" --train-queries "word_string.str.len()>7 and block in [1, 3, 5]" > Logs_GAT/gat_word_length_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='he' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" --test-queries "word_string=='boy' and block in [2, 4, 6]" --test-queries "word_string=='girl' and block in [2, 4, 6]" > Logs_GAT/gat_he_she_boy_girl_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "Question_type_subject_object==1 and block in [2, 4, 6] and word_position==-1" --train-queries "sentence_length==5 and Declarative==1 and block in [2, 4, 6] and word_position==-1" > Logs_GAT/gat_object_question_dec_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all -s UCLA -p patient_502 -k all -s UCLA -p patient_505 -k all --train-queries "word_string=='who' and block in [2, 4, 6]" --train-queries "word_string=='she' and block in [2, 4, 6]" > Logs_GAT/gat_who_she_audio.log 2>&1 &



