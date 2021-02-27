from chatbot import chatbot
from flask import Flask, render_template, request
from collections import defaultdict
import sys
import pickle
from senti.nb import preprocess, prediction
import re

app = Flask(__name__)
app.static_folder = 'static'
responses=["Hi Name, that's a nice name!","So Name, how are you feeling today?"]

class NaiveBayesClassifier(object):
    def __init__(self, n_gram=1, printing=False):
        self.prior = defaultdict(int)
        self.logprior = {}
        self.bigdoc = defaultdict(list)
        self.loglikelihoods = defaultdict(defaultdict)
        self.V = []
        self.n = n_gram

    def predict(self, test_doc):
        sums={0:0, 4:0}
        for c in self.bigdoc.keys():
            sums[c]=self.logprior[c]
            words=test_doc.split(" ")
            for word in words:
                if word in self.V:
                    sums[c]+=self.loglikelihoods[c][word]
        return sums

@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    global iter, name
    userText = request.args.get('msg')
    response=""
    if iter==0:
        name=userText
        response=re.sub("Name",name,responses[iter])
        iter+=1
    elif iter==1:
        response=re.sub("Name",name,responses[iter])
        iter+=1
    elif iter==2:
        text=preprocess(userText)
        if prediction(text, model)==4:
           response="Oh, that's good to hear!" 
        else:
            response="I am sorry to hear that! <Quote here>"
        response+="\nBtw, What do you do in your free time?"
        iter+=1
    else:
        response="It was great talking to you! Have a good day!"
    return response
    """text = nb.preprocess(userText)
    print(nb.prediction(text, model), file=sys.stderr)
    #return str(chatbot.get_response(userText))
    return text+nb.prediction(text, model)"""

@app.route("/chatbot")
def show_chatbot():
    return render_template("index.html")

if __name__ == "__main__":
    with open('senti\model.sav', 'rb') as f_in:
        model = pickle.load(f_in)
    f_in.close()
    iter=0
    name=""
    app.run() 
