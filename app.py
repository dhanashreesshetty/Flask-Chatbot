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
from NN.covid import covid
import sys
from Recommendation.quotes import scrape
from Recommendation.songs import songs
from Recommendation.movies import fetch_movies
from Recommendation.books import book_select 

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
app.config['MYSQL_PASSWORD'] = 'Vesit@123'
app.config['MYSQL_DB'] = 'users'
  
mysql = MySQL(app) 

responses=["Greeting Name, that's a nice name!","So Name, how are you feeling today?",
["Oh, that's wonderful!😇","It's a pleasure to see you in a good mood😍","That's so good to hear💚" ],
["I am sorry to hear that😔", "Oh! that's sad😕"],"What do you think is the reason behind that?", 
["That's too bad😓 But hey! As it is rightly said, you are bigger and better than whatever is intimidating, scaring or hurting you! So don't lose hope!",
"That's too bad😓 But hey! As Bob Marley said, you never know how strong you are, until being strong is your only choice. So keep going!"],
"Would you like to chat more?$Yes$No","Thank you for answering these questions, Name! %",
"It was great talking to you! Have a good day! Would you like to get some recommendations to stay positive?$Show Recommendation$No Thank You$ok",
"Is your negative mood related to Covid-19 pandemic?$yes$no",
"What could be the possible causes for your anxiety?$Lockdown/Isolation$Loss of Loved one(s)$You have tested +ve$Negative Environment$Can't Say" ]

phq9=["We would like to ask you a few questions. How often do you find that you have little interest or pleasure in doing things?#"
,"Are you feeling down, depressed, or hopeless?#","Do you have trouble falling or staying asleep, or are you sleeping too much?#","Are you feeling tired or having little energy?#",
"Do you have poor appetite or are overeating?#","Are you feeling bad about yourself, or that you are a failure or have let yourself or your family down?#",
"Do you have trouble concentrating on things, such as reading the newspaper or watching television?#",
"Have you been moving or speaking so slowly that other people have noticed, or the opposite?#","Do you find yourself having thoughts that you would be better off dead, or of hurting yourself?#"
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




    

@app.route("/get",methods=['GET', 'POST'])
def get_bot_response():
    global iter, name, pred ,phq , tag1
    counter=0
    tag1="joy"
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
            tag1='joy'
            print("4 - Positive")
            iter=9
        else:
            iter+=1
            print("0 - Negative")
            response=random.choice(responses[iter])+responses[iter+1]
            iter=5
    elif iter==5:
        resp=classify(userText)
        x=covid(userText)
        print(x)
        tag1=resp
        print(resp)
        print("ppp",user)
        #detect sentiment of usertext to use in recommendation model here
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE  account SET emotion = (% s) WHERE username = (% s) ', (tag1,session['user'],)) 
        mysql.connection.commit() 
        ##############################################################################
        if x=="Yes":
            response=responses[9]
            iter=10
        else:
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
            #books
            book_display=book_select(str(tag1))
            session['books1']=book_display[0:4]
            session['books2']=book_display[4:]
            #movies
            movies = fetch_movies(str(tag1))
            session['movies1']=movies[0:4]
            session['movies2']=movies[4:]
            iter=12
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
            iter=9

    elif iter==9:
        #stat = request.json.get('phq_score_send')
        print(stat)
        response=responses[8]
        quote_ans=scrape(1,str(tag1))
        session['quotes1']=quote_ans[0:4]
        session['quotes2']=quote_ans[4:]
        #music
        song_ans=songs(tag1)
        session['songs1']=song_ans[0:4]
        session['songs2']=song_ans[4:]
        print(song_ans)
        #books
        book_display=book_select(str(tag1))
        session['books1']=book_display[0:4]
        session['books2']=book_display[4:]
        #movies
        movies = fetch_movies(str(tag1))
        session['movies1']=movies[0:4]
        session['movies2']=movies[4:]
        iter=12
        
    elif iter==10:
        if(userText=="Yes"):
            response=responses[10]
            iter=11
        elif (userText=="No"):
            response=responses[6]
            iter=7

    elif iter==11:
        if(userText=="Lockdown/Isolation"):
            response="Here are some ways to beat the lockdown blues and create a virtual support network : <a href='https://www.mentalhealth.org.uk/coronavirus/loneliness-during-coronavirus' target='_blank'>Ways to overcome loneliness</a> .<br><br> Always remember to open up to friends and family around you. We hope you will be benefited from these tips. Is there anything else you would like to share?"
        elif (userText=="Loss of Loved ones"):
            response="We cannot imagine the amount of pain you are going through. We would just like you to know that it is okay to grieve and let the sadness wash over you. The pain will lessen little by little and one day you will remember only the happy memories with them. Hang in there and here are some resources to give you support: <a href='https://coronavirus.beyondblue.org.au/managing-my-daily-life/coping-with-grief-and-loss/grieving-the-loss-of-a-loved-one-during-the-coronavirus-pandemic.html' target='_blank'>Grieving loss of a loved one.</a>.<br><br>Is there anything else you would like to share?"
        elif (userText=="You have tested +ve"):
            response="This is a tough situation but nothing you can't overcome. Believing in yourself and following proper nutrition guidelines will make this quarantine easier for you: <a href='https://www.euro.who.int/en/health-topics/health-emergencies/coronavirus-covid-19/publications-and-technical-guidance/food-and-nutrition-tips-during-self-quarantine' target='_blank'>Nutrition tips during quarantine</a> <br><br>Stay safe and get well soon. Is there anything else you would like to share?"
        elif (userText=="Negative Environment"):
            response="In this digital age, more connectivity has unfortunately resulted in increased spread of devastating news and panic mongering by sensational news bulletins. There are ways in which you can stay away from negative sources:<a href='https://www.narayanahealth.org/blog/tips-to-overcome-coronavirus-related-stress/' target='_blank'>Protecting yourself from overexposure to negative news</a>.<br><br> Is there anything else you would like to share?"
        elif (userText=="Can't Say"):
            response="Here are some covid mental health guidelines for you to understand the issues you are facing and how to overcome them: <a href='https://www.helplinecenter.org/2-1-1-community-resources/helpsheets/covid-19-and-your-mental-health/' taget='_blank'>Covid Helpline</a> . Is there anything else you would like to share?"
        iter =9

    elif iter==12:
        if(userText=="No Thank You"):
            response="No problem! Have a nice day."

        
    return response
    
@app.route("/show_chatbot")
def show_chatbot():
    return render_template("index.html")

@app.route("/show_recommendation")
def show_recommendation():
    return render_template("recommendation.html",quotes1=get_quotes1(),quotes2=get_quotes2(),songs1=session['songs1'],songs2=session['songs2'],movies1=session['movies1'],movies2=session['movies2'],books1=session['books1'],books2=session['books2'])

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
        session['user']=username
        password = request.form['password'] 
        email = request.form['email'] 
        if email!="":
            print(username,password,email)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM account WHERE username = % s', (username, )) 
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
                cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s,% s,% s)', (username, password, email,"happy","minimal" )) 
                mysql.connection.commit() 
                msg = 'You have successfully registered !'
                return render_template('index.html')

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM account WHERE username = % s AND password = % s', (username, password, )) 
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
    user=""
    app.run(debug=True) 