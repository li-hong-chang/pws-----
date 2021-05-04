# BeautifulSoup4
# requests

import requests
from bs4 import BeautifulSoup

re = requests.get('https://movies.yahoo.com.tw/')
#print(re)
#print(re.text)

soup_movie = BeautifulSoup(re.text, 'html.parser')
#print(soup)

#print(soup.title)
#print(soup.find('title'))
#print(soup.title.text)
#print(soup.title.string)

#print(soup.find_all('a'))

# 
all_movies = soup_movie.find_all('div', {'class': 'movielist_info'})
for movie in all_movies:
    url_movie = movie.a['href']
    name = movie.find('h2').text
    on  = movie.find('h3').text
    print(name, on)
