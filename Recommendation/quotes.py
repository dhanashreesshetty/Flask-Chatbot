from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import random

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
    author = i.find('span',attrs={'class':'authorOrTitle'}).text.strip()
    q="--------".join([quote, author])
    if len(q)<300:
      quotes.append(q)
    authors.append(author)
  quotes_display=[]
  if len(quotes)>0:
    for i in range(8):
      quotes_display.append(quotes[i])
  return quotes_display
"""scrape(1,"fear")"""