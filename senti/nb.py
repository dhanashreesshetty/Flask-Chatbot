import pandas as pd
import numpy as np
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *

def remove_pattern(input_txt, pattern):
    print(1)
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

def preprocess(line):
    tidy_line = remove_pattern(line, "@[\w]*") #remove user mentions

    tidy_line = tidy_line.str.replace("[^a-zA-Z#]", " ") #remove punctuation

    tokenized = word_tokenize(tidy_line) # tokenize

    #stem
    stemmer = PorterStemmer()
    stemmed=[]
    for word in tokenized:
        stemmed.append(stemmer.stem(word))

    stemmed_line = ' '.join(stemmed)

    #NBclassifier.predict(stemmed_line)
