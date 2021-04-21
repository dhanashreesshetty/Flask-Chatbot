from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
from collections import defaultdict
import pickle
from senti.nb import preprocess, prediction
import re
import datetime
import random
from NN.neural import classify
import sys
from Recommendation.quotes import scrape
from Recommendation.songs import songs

app = Flask(__name__)
app.static_folder = 'static'
from flask_session import Session

app.config['SECRET_KEY'] = "some_random"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT']= False

Session(app)

app.secret_key = 'your secret key'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'users'
  
mysql = MySQL(app) 

responses=["Greeting Name, that's a nice name!","So Name, how are you feeling today?",
["Oh, that's wonderful!😇","It's a pleasure to see you in a good mood😍","That's so good to hear💚" ],
["I am sorry to head that😔", "Oh! that's sad😕"],"What do you think is the reason behind that?", 
["That's too bad😓 But hey! As it is rightly said, you are bigger and better than whatever is intimidating, scaring or hurting you! So don't lose hope!",
"That's too bad😓 But hey! As Bob Marley said, you never know how strong you are, until being strong is your only choice. So keep going!"],
"Would you like to chat more?$Yes$No","Thank You for answering questions,Name!So our analysis is .%",
"It was great talking to you! Have a good day!Woud you like to see some recommendation to stay positive?$Show Recommendation$No Thank You$ok"]

phq9=["We would like to ask u a few questions and would like you to rate them on a scale of 1-4                 Little Interest or Plasure in doing things?#"
,"Feeling down, depressed,or hopeless#","Trouble in falling or staying asleep or sleeping too much#","Feeling tired or having little energy#",
"Poor appetite or overeating#","Feeling bad about yourself or that you are a failure or have let yourself or your family down#",
"Trouble concertrating on things,such as reading the newspaper or watching television#",
"Moving or speaking so slowly that other people could have noticed or opposite#","Thoughts that you would be better off dead or of hurting yourself#"
]

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


#def phq9que():
@app.route("/get")

def get_bot_response():
    global iter, name, pred ,phq , tag1
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
        resp=classify(userText)
        tag1=resp
        print(resp)
        #detect sentiment of usertext to use in recommendation model here
        response=random.choice(responses[iter])
        iter+=1
    elif iter==6:
        response=responses[iter]
        iter+=1
        #Yes/No question. If yes, direct to phq-9 questionnaire
    elif iter==7:
        print(userText,file=sys.stderr)
        if(userText=="No"):
            response=responses[iter+1]
            quote_ans=scrape(1,str(tag1))
            session['quotes1']=quote_ans[0:4]
            session['quotes2']=quote_ans[4:]
            #music
            song_ans=songs(tag1)
            session['songs1']=song_ans[0:4]
            session['songs2']=song_ans[4:]
            print(song_ans)
            iter=9
        elif(userText=="Yes"):
            response=phq9[phq]
            phq=phq+1
            iter+=1

    elif iter==8:
        if phq<9:
            response=phq9[phq]
            phq=phq+1
        else:
            response=re.sub("Name",name,responses[7])

    elif iter==9:
        #print(userText,file=sys.stderr)
        if(userText=="No"):
            response=responses[iter]
        elif(userText=="Yes"):
            quote_ans=scrape(1,tag1)
    return response
   
@app.route("/show_chatbot")
def show_chatbot():
    return render_template("index.html")

@app.route("/show_recommendation")
def show_recommendation():
    return render_template("recommendation.html",quotes1=get_quotes1(),quotes2=get_quotes2(),songs1=session['songs1'],songs2=session['songs2'])

def get_quotes1():
    quotes1=session['quotes1']
    return quotes1
def get_quotes2():
    quotes2=session['quotes2']
    return quotes2


@app.route('/loginregister', methods =['GET', 'POST']) 
def loginregister(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        if email!="":
            print(username,password,email)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
            account = cursor.fetchone() 
            if account: 
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username): 
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email: 
                msg = 'Please fill out the form !'
            else: 
                cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, )) 
                mysql.connection.commit() 
                msg = 'You have successfully registered !'
                return render_template('index.html')

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
            account = cursor.fetchone() 
            if account: 
                session['loggedin'] = True
                session['id'] = account['id'] 
                session['username'] = account['username']
                msg = 'Logged in successfully !'
                return render_template('index.html') 
            else: 
                msg = 'Incorrect username / password !'

    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
        
    return render_template('home.html', msg = msg)
    


if __name__ == "__main__":
    with open('senti\model.sav', 'rb') as f_in:
        model = pickle.load(f_in)
    f_in.close()
    iter=0
    phq =0
    quote_ans=["hello"]
    name=""
    app.run(debug=True) 