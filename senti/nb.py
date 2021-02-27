import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import sys

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

def preprocess(line):
    tidy_line = re.sub("[^a-zA-Z]", " ", line) #remove punctuation
    print("After removing punctuation: ", tidy_line, file=sys.stderr)
    tokenized = word_tokenize(tidy_line) # tokenize
    print("After tokenizing: ", tokenized, file=sys.stderr)
    #stem
    stemmer = PorterStemmer()
    stemmed=[]
    for word in tokenized:
        stemmed.append(stemmer.stem(word))
    stemmed_line = ' '.join(stemmed)
    print("After stemming: ", stemmed_line, file=sys.stderr)
    return stemmed_line

def prediction(text, model):
    probabilities = model.predict(text)
    print("Probabilities: ", probabilities, file=sys.stderr)
    if probabilities[0] <= probabilities[4]:
        prediction = 4
    else:
        prediction = 0
    return prediction
        
