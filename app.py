from chatbot import chatbot
from flask import Flask, render_template, request
from senti.nb import remove_pattern

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    print(1)
    print(remove_pattern("@usa", "@[\w]*"))
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

@app.route("/chatbot")
def show_chatbot():
    return render_template("index.html")

if __name__ == "__main__":
    app.run() 
