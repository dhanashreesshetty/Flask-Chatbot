from flask import Flask, render_template, request
from collections import defaultdict
import pickle
from senti.nb import preprocess, prediction
import re
import datetime
import random

app = Flask(__name__)
app.static_folder = 'static'
responses=["Greeting Name, that's a nice name!","So Name, how are you feeling today?",
["Oh, that's wonderful!😇","It's a pleasure to see you in a good mood😍","That's so good to hear💚" ],
["I am sorry to hear that😔", "Oh! that's sad😕"],"What do you think is the reason behind that?", 
["That's too bad😓 But hey! As it is rightly said, you are bigger and better than whatever is intimidating, scaring or hurting you! So don't lose hope!",
"That's too bad😓 But hey! As Bob Marley said, you never know how strong you are, until being strong is your only choice. So keep going!"],
"Would you like to chat more?","It was great talking to you! Have a good day!"]

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
    global iter, name, pred
    userText = request.args.get('msg')
    response=""
    if iter==0:
        name=userText
        greet=""
        hour=datetime.datetime.now().hour
        if hour < 12:
            greet='Good morning'
        elif 12 <= hour < 18:
            greet='Good afternoon'
        else:
            greet='Good evening'
        response=re.sub("Name",name,responses[iter])
        response=re.sub("Greeting",greet,response)
        iter+=1
    elif iter==1:
        response=re.sub("Name",name,responses[iter])
        iter+=1
    elif iter==2:
        text=preprocess(userText)
        if prediction(text, model)==4:
            response=random.choice(responses[iter])
            iter=7
        else:
            iter+=1
            response=random.choice(responses[iter])+responses[iter+1]
            iter=5
    elif iter==5:
        #detect sentiment of usertext to use in recommendation model here
        response=random.choice(responses[iter])
        iter+=1
    elif iter==6:
        response=responses[iter]
        iter+=1
        #Yes/No question. If yes, direct to phq-9 questionnaire
    elif iter==7:
        response=responses[iter]
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
    pred=-1
    app.run() 
