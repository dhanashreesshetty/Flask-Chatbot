import pandas as pd
import numpy as np
import re
from collections import defaultdict
import pickle

dataset=pd.read_csv('data.csv',encoding='ISO-8859-1')

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

dataset['tidy_line'] = np.vectorize(remove_pattern)(dataset['line'], "@[\w]*") #remove user mentions

dataset['tidy_line'] = dataset['tidy_line'].str.replace("[^a-zA-Z#]", " ") #remove punctuation

tokenized_line = dataset['tidy_line'].apply(lambda x: x.split()) # tokenize

#stem
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer(language='english')
tokenized_line = tokenized_line.apply(lambda x: [stemmer.stem(i) for i in x])

for i in range(len(tokenized_line)):
    tokenized_line[i] = ' '.join(tokenized_line[i])

dataset['tidy_line'] = tokenized_line

#Split dataset into training and testing data
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(dataset['tidy_line'], dataset['label'], test_size=0.3, random_state=0)

class NaiveBayesClassifier(object):
    def __init__(self, n_gram=1, printing=False):
        self.prior = defaultdict(int)
        self.logprior = {}
        self.bigdoc = defaultdict(list)
        self.loglikelihoods = defaultdict(defaultdict)
        self.V = []
        self.n = n_gram

    def compute_prior_and_bigdoc(self, xtrain, ytrain):
        for x, y in zip(xtrain, ytrain):
            all_words = x.split(" ")
            if self.n == 1:
                grams = all_words
            else:
                grams = self.words_to_grams(all_words)

            self.prior[y] += len(grams)
            self.bigdoc[y].append(x)

    def compute_vocabulary(self, data):
        vocabulary=set()
        for d in data:
            for word in d.split(" "):
                vocabulary.add(word.lower())
        return vocabulary

    def count_word_in_classes(self):
        counts = {}
        for c in list(self.bigdoc.keys()):
            docs=self.bigdoc[c]
            counts[c]=defaultdict(int)
            for doc in docs:
                words=doc.split(" ")
                for word in words:
                    counts[c][word]+=1
        return counts

    def train(self, xtrain, ytrain, alpha=1):
        N_doc=len(xtrain)

        self.V=self.compute_vocabulary(xtrain)

        for x, y in zip(xtrain,ytrain):
            self.bigdoc[y].append(x)

        all_classes=set(ytrain)

        self.word_count=self.count_word_in_classes()

        for c in all_classes:
            N_c=float(sum(ytrain==c))

            self.logprior[c]=np.log(N_c/N_doc)

            total_count=0
            for word in self.V:
                total_count+=self.word_count[c][word]

            for word in self.V:
                count=self.word_count[c][word]
                self.loglikelihoods[c][word]=np.log((count+alpha)/(total_count+alpha+len(self.V)))

    def predict(self, test_doc):
        sums={0:0, 4:0}
        for c in self.bigdoc.keys():
            sums[c]=self.logprior[c]
            words=test_doc.split(" ")
            for word in words:
                if word in self.V:
                    sums[c]+=self.loglikelihoods[c][word]
        return sums

def evaluate_predictions(xtest,ytest,trained_classifier):
      correct_predictions = 0
      predictions_list = []
      prediction = -1
      preds=[]

      for dataset,label in zip(xtest, ytest):
        probabilities = trained_classifier.predict(dataset)
        if probabilities[0] >= probabilities[4]:
            prediction = 0
        else:
            prediction = 4
        preds.append(prediction)

        if prediction == label:
          correct_predictions += 1
          predictions_list.append("+")
        else:
          predictions_list.append("-")

      #print(preds)
      print("Predicted correctly {} out of {} ({}%)".format(correct_predictions,len(ytest),round(correct_predictions/len(ytest)*100,5)))
      return predictions_list, round(correct_predictions/len(ytest)*100)

NBclassifier = NaiveBayesClassifier()
NBclassifier.train(xtrain, ytrain, alpha=1)
results, acc = evaluate_predictions(xtest, ytest, NBclassifier)

##dump the model into a file
with open("snowmodel.sav", 'wb') as f_out:
    pickle.dump(NBclassifier, f_out) # write final_model in .bin file
    f_out.close()  # close the file 


