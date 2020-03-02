import os

###VOWEL QUALITY
VOWELS = {}
VOWELS['TNS'] = "IY1 IY2 IY0 EY1 EY2 EY0 EYR1 EYR2 EYR0 OW1 OW2 OW0 UW1 UW2 UW0"
VOWELS['LAX'] = "IH1 IH2 IH0 IR1 IR2 IR0 EH1 EH2 EH0 AH1 AH2 AH0 AE1 AE2 AE0 AY1 AY2 AY0 AW1 AW2 AW0 AA1 AA2 AA0 AAR1 AAR2 AAR0 AO1 AO2 AO0 OY1 OY2 OY0 OR1 OR2 OR0 ER1 ER2 ER0 UH1 UH2 UH0 UR1 UR2 UR0"
VOWELS['UNR'] = "IY1 IY2 IY0 IH1 IH2 IH0 IR1 IR2 IR0 EY1 EY2 EY0 EYR1 EYR2 EYR0 EH1 EH2 EH0 AH1 AH2 AH0 AE1 AE2 AE0 AY1 AY2 AY0 AA1 AA2 AA0 AAR1 AAR2 AAR0"
VOWELS['RND'] = "AW1 AW2 AW0 AO1 AO2 AO0 OW1 OW2 OW0 OY1 OY2 OY0 OR1 OR2 OR0 ER1 ER2 ER0 UH1 UH2 UH0 UW1 UW2 UW0 UR1 UR2 UR0"
VOWELS['BCK'] = "AA1 AA2 AA0 AAR1 AAR2 AAR0 AO1 AO2 AO0 OW1 OW2 OW0 OY1 OY2 OY0 OR1 OR2 OR0 UH1 UH2 UH0 UW1 UW2 UW0 UR1 UR2 UR0"
VOWELS['CNT'] = "AH1 AH2 AH0 AY1 AY2 AY0 AW1 AW2 AW0 ER1 ER2 ER0"
VOWELS['FRO'] = "IY1 IY2 IY0 IH1 IH2 IH0 IR1 IR2 IR0 EY1 EY2 EY0 EYR1 EYR2 EYR0 EH1 EH2 EH0 AE1 AE2 AE0"
VOWELS['HI'] = "IY1 IY2 IY0 IH1 IH2 IH0 IR1 IR2 IR0 UH1 UH2 UH0 UW1 UW2 UW0 UR1 UR2 UR0"
VOWELS['MID'] = "EY1 EY2 EY0 EYR1 EYR2 EYR0 EH1 EH2 EH0 AH1 AH2 AH0 AO1 AO2 AO0 OW1 OW2 OW0 OY1 OY2 OY0 OR1 OR2 OR0 ER1 ER2 ER0"
VOWELS['LOW'] = "AE1 AE2 AE0 AY1 AY2 AY0 AW1 AW2 AW0 AA1 AA2 AA0 AAR1 AAR2 AAR0"
VOWELS['DIPH'] = "AY1 AY2 AY0 AW1 AW2 AW0 OY1 OY2 OY0"

###VOWEL STRESS
VOWELS['STR'] = "IY1 IH1 IR1 EY1 EYR1 EH1 AH1 AE1 AY1 AW1 AA1 AAR1 AO1 OW1 OY1 OR1 ER1 UH1 UW1 UR1"
VOWELS['2ND'] = "IY2 IH2 IR2 EY2 EYR2 EH2 AH2 AE2 AY2 AW2 AA2 AAR2 AO2 OW2 OY2 OR2 ER2 UH2 UW2 UR2"
VOWELS['UNS'] = "IY0 IH0 IR0 EY0 EYR0 EH0 AH0 AE0 AY0 AW0 AA0 AAR0 AO0 OW0 OY0 OR0 ER0 UH0 UW0 UR0"

###CONSONANT PLACE
CONSONANTS = {}
#CONSONANTS['COR'] = "DENT ALV POSTALV PAL LIQ"
#CONSONANTS['LAB'] = "BILAB LABDENT W"
#CONSONANTS['DOR'] = "VEL W"
CONSONANTS['COR'] = "TH DH T D S Z N CH JH SH ZH Y L R"
CONSONANTS['LAB'] = "P B M F V W"
CONSONANTS['DOR'] = "K G NG W"
CONSONANTS['BILAB'] = "P B M"
CONSONANTS['LABDENT'] = "F V"
CONSONANTS['DENT'] = "TH DH"
CONSONANTS['ALV'] = "T D S Z N"
CONSONANTS['PLV'] = "CH JH SH ZH"
CONSONANTS['PAL'] = "Y"
CONSONANTS['VEL'] = "K G NG"
CONSONANTS['LAR'] = "HH"

###CONSONANT MANNER
CONSONANTS['STOP'] = "P T K B D G"
CONSONANTS['AFFR'] = "CH JH"
CONSONANTS['FRIC'] = "F TH S SH HH V DH Z ZH"
CONSONANTS['NAS'] = "M N NG"
CONSONANTS['LIQ'] = "L R"
CONSONANTS['SIB'] = "CH S SH JH Z ZH"
CONSONANTS['GLI'] = "W Y"

###CONSONANT VOICING/SONORANCE
CONSONANTS['VLS'] = "P T K CH F TH S SH HH"
CONSONANTS['VOI'] = "B D G JH V DH Z ZH"
CONSONANTS['SON'] = "M N NG L W R Y"

for channel in list(range(9, 17)) + list(range(40, 48)):
    cmd = "python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/plot_evoked_comparison.py -patient 479_11 -channel %i" % channel
    for poa in ['COR', 'LAB', 'DOR']:
        curr_class = CONSONANTS[poa].split(' ')
        curr_class = ['"' + s.strip(' ') + '"' for s in curr_class]
        curr_str = "'phone_string in [%s]" % (', '.join(curr_class))
        cmd += " --queries-to-compare %s %s" % (poa, curr_str)
        cmd += " and block in [2, 4, 6]'"
    print(cmd)
    os.system(cmd)

    cmd = "python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/plot_evoked_comparison.py -patient 479_11 -channel %i" % channel
    for poa in ['STOP', 'AFFR', 'FRIC', 'NAS', 'LIQ', 'SIB', 'GLI']:
        curr_class = CONSONANTS[poa].split(' ')
        curr_class = ['"' + s.strip(' ') + '"' for s in curr_class]
        curr_str = "'phone_string in [%s]" % (', '.join(curr_class))
        cmd += " --queries-to-compare %s %s" % (poa, curr_str)
        cmd += " and block in [2, 4, 6]'"
    print(cmd)
    os.system(cmd)

    cmd = "python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/plot_evoked_comparison.py -patient 479_11 -channel %i" % channel
    for poa in ['VLS', 'VOI', 'SON']:
        curr_class = CONSONANTS[poa].split(' ')
        curr_class = ['"' + s.strip(' ') + '"' for s in curr_class]
        curr_str = "'phone_string in [%s]" % (', '.join(curr_class))
        cmd += " --queries-to-compare %s %s" % (poa, curr_str)
        cmd += " and block in [2, 4, 6]'"
    print(cmd)
    os.system(cmd)

