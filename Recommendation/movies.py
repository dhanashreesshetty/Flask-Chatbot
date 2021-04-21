import json
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

comedy = "https://www.imdb.com/search/title/?genres=comedy"
romance = "https://www.imdb.com/search/title/?genres=romance"
adventure = "https://www.imdb.com/search/title/?genres=adventure"
animation = "https://www.imdb.com/search/title/?genres=animation"
fantasy = "https://www.imdb.com/search/title/?genres=fantasy"

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
        link = header.find('a')
        ref = link["href"]
        span = div.find('span', attrs={'class': 'genre'})
        image = div.find('div', attrs={'class': 'lister-item-image float-left'})
        poster = image.find('img')
        ref2 = poster["loadlate"]
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

#get_movies(comedy, 'movie_data/comedy.json', 100)
#get_movies(romance, 'movie_data/romance.json', 100)
#get_movies(adventure, 'movie_data/adventure.json', 100)
#get_movies(animation, 'movie_data/animation.json', 100)
#get_movies(fantasy, 'movie_data/fantasy.json', 100)

def fetch_songs():
    f = open('C:\Flask-Chatbot\Recommendation\movie_data\comedy.json', 'r')
    data = json.load(f)
    movies = []
    for i in range(8):
        movies.append(random.choice(data))
    return movies
