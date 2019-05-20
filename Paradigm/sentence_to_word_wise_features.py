import pandas, os, pickle
# Read features file ('xlsx') and word2POS pickles
sheet = pandas.read_excel('features_sentence_wise_patient_479.xlsx')
headers = sheet.columns
num_columns = len(headers)
word2POS = pickle.load(open('word2POS.pkl', 'r'))
word2POS_simplified = pickle.load(open('word2POS_simplified.pkl', 'r'))

# Break down sentence into words. Add features into the fields of each work
word_strings = []; sentence_numbers = []; features = []
for rw in range(len(sheet['Trial number'])):
    sentence_number = sheet['Trial number'][rw]
    sentence = sheet['Sentence'][rw]
    words = sentence.split(' ')
    for w, word in enumerate(words):
        word = word.strip().strip('?').strip('.').lower()
        sentence_numbers.append(int(sentence_number))
        word_strings.append(word)
        fields = ''  # feature fields for word
        for i, header in enumerate(headers):
            if i > 1:
                fields += str(sheet[header][rw]) + '\t'
        fields += str(w) + '\t' + word2POS[word] + '\t' + word2POS_simplified[word]
        features.append(fields)
    sentence_numbers.append(int(sentence_number))
    word_strings.append('')
    fields = '' # feature fields for end-of-sentence
    for i, header in enumerate(headers):
        if i > 1:
            fields += str(sheet[header][rw]) + '\t'
    features.append(fields)

# Write all into a tab-delimited text file
headers = list(headers) + ['word_number'] + ['POS'] + ['POS_simplified']
numbering = [str(i+1) for i in range(len(headers))]
with open('features_word_wise_patient_479.txt', 'w') as f:
    curr_line = '\t'.join(map(str, numbering)) + '\n'
    f.writelines(curr_line)
    curr_line = '\t'.join(map(str, headers)) + '\n'
    f.writelines(curr_line)
    for i in range(len(sentence_numbers)):
        curr_line = str(sentence_numbers[i]) + '\t' + word_strings[i] + '\t' + features[i] + '\n'
        f.writelines(curr_line)
