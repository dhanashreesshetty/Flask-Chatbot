from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request

authors =[]
quotes =[]


def scrape(page_number,tag):
  page_num = str(page_number)
  url='https://www.goodreads.com/quotes/tag/'+tag+'?page='+page_num
  webpage = requests.get(url)
  soup = BeautifulSoup(webpage.text , 'html.parser')
  quoteText= soup.find_all('div',attrs={'class':'quoteText'})

  for i in quoteText:
    quote = i.text.strip().split('\n')[0]
    print(quote)
    author = i.find('span',attrs={'class':'authorOrTitle'}).text.strip()
    print(author)
    quotes.append(quote)
    authors.append(author)

print(quotes)
#scrape(1,fear)