# BASH

for PATIENT in '479_11' '482' '493' '502' '504' '505'; do
    python generate_logs_with_phonemes.py --patient $PATIENT
done
