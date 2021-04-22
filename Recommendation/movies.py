import json
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

comedy = "https://www.imdb.com/search/title/?genres=comedy"
action = "https://www.imdb.com/search/title/?genres=action"
thriller = "https://www.imdb.com/search/title/?genres=thriller"
drama = "https://www.imdb.com/search/title/?genres=drama"
romance = "https://www.imdb.com/search/title/?genres=romance"
adventure = "https://www.imdb.com/search/title/?genres=adventure"
animation = "https://www.imdb.com/search/title/?genres=animation"
fantasy = "https://www.imdb.com/search/title/?genres=fantasy"
romcom = "https://www.imdb.com/search/title/?genres=comedy,romance"
comact = "https://www.imdb.com/search/title/?genres=action,comedy"
superhero = "https://www.imdb.com/search/keyword/?keywords=superhero"

def get_web_page_content(url):
    req = Request(url, headers={'User-Agent':'Edge'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup

def get_movies(url, file_name, nos):
    soup = get_web_page_content(url)
    divs = soup.find('div', attrs={'class': 'lister-list'})
    movies = []
    i = 1
    for div in divs.findAll('div', attrs={'class': 'lister-item mode-advanced'}):
        movie = {}
        header = div.find('h3', attrs={'class': 'lister-item-header'})
        id = header.find('span', attrs={'class': 'lister-item-index unbold text-primary'})
        link = header.find('a')
        ref = link["href"]
        span = div.find('span', attrs={'class': 'genre'})
        image = div.find('div', attrs={'class': 'lister-item-image float-left'})
        poster = image.find('img')
        ref2 = poster["loadlate"]
        movie['id'] = id.text.strip()
        movie["imdb_link"] = "https://www.imdb.com" + ref
        movie["title"] = link.text.strip()
        movie["genre"] = span.text.strip()
        movie["poster"] = ref2
        movies.append(movie)
        i+=1
        if i>nos:
            break
    
    with open(file_name, 'w') as outfile:
        json.dump(movies, outfile, indent=4)

#get_movies(comedy, 'movie_data/comedy.json', 50)
#get_movies(action, 'movie_data/action.json', 50)
#get_movies(thriller, 'movie_data/thriller.json', 50)
#get_movies(drama, 'movie_data/drama.json', 50)
#get_movies(romance, 'movie_data/romance.json', 50)
#get_movies(adventure, 'movie_data/adventure.json', 50)
#get_movies(animation, 'movie_data/animation.json', 50)
#get_movies(fantasy, 'movie_data/fantasy.json', 50)
#get_movies(romcom, 'movie_data/romcom.json', 50)
#get_movies(comact, 'movie_data/comact.json', 50)

def fetch_movies(emotion):
    movies = []
    if(emotion == 'joy'):
        f1=open('C:\Flask-Chatbot\Recommendation\movie_data/adventure.json', 'r')
        f2=open('C:\Flask-Chatbot\Recommendation\movie_data/drama.json', 'r')
        f3=open('C:\Flask-Chatbot\Recommendation\movie_data/romcom.json', 'r')
        f4=open('C:\Flask-Chatbot\Recommendation\movie_data/fantasy.json', 'r')
        adventure = json.load(f1)
        drama = json.load(f2)
        romcom = json.load(f3)
        superhero = json.load(f4)
        for i in range(2):
            movies.append(random.choice(adventure))
            movies.append(random.choice(drama))
            movies.append(random.choice(romcom))
            movies.append(random.choice(superhero))
    elif(emotion == 'sadness'):
        f1=open('C:\Flask-Chatbot\Recommendation\movie_data/animation.json', 'r')
        f2=open('C:\Flask-Chatbot\Recommendation\movie_data/fantasy.json', 'r')
        f3=open('C:\Flask-Chatbot\Recommendation\movie_data/thriller.json', 'r')
        f4=open('C:\Flask-Chatbot\Recommendation\movie_data/comedy.json', 'r')
        animation = json.load(f1)
        fantasy = json.load(f2)
        thriller = json.load(f3)
        comedy = json.load(f4)
        for i in range(2):
            movies.append(random.choice(animation))
            movies.append(random.choice(fantasy))
            movies.append(random.choice(thriller))
            movies.append(random.choice(comedy))
    elif(emotion == "fear"):
        f1=open('C:\Flask-Chatbot\Recommendation\movie_data/animation.json', 'r')
        f2=open('C:\Flask-Chatbot\Recommendation\movie_data/comedy.json', 'r')
        f3=open('C:\Flask-Chatbot\Recommendation\movie_data/comact.json', 'r')
        f4=open('C:\Flask-Chatbot\Recommendation\movie_data/romcom.json', 'r')
        animation = json.load(f1)
        comedy = json.load(f2)
        comact = json.load(f3)
        romcom = json.load(f4)
        for i in range(2):
            movies.append(random.choice(animation))
            movies.append(random.choice(comedy))
            movies.append(random.choice(comact))
            movies.append(random.choice(romcom))
    elif(emotion == 'anger'):
        f1=open('C:\Flask-Chatbot\Recommendation\movie_data/thriller.json', 'r')
        f2=open('C:\Flask-Chatbot\Recommendation\movie_data/animation.json', 'r')
        f3=open('C:\Flask-Chatbot\Recommendation\movie_data/adventure.json', 'r')
        f4=open('C:\Flask-Chatbot\Recommendation\movie_data/drama.json', 'r')
        thriller = json.load(f1)
        animation = json.load(f2)
        adventure = json.load(f3)
        drama = json.load(f4)
        for i in range(2):
            movies.append(random.choice(thriller))
            movies.append(random.choice(animation))
            movies.append(random.choice(adventure))
            movies.append(random.choice(drama))
    return movies
