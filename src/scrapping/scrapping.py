import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

headers = ({
    #Check your information through http://httpbin.org/get
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept-Language' : 'en-US, en;q=0.5' 
})

movie_id = []
movie_name = []
year = []
time=[]
rating=[]
metascore =[]
director=[]
votes = []
gross = []
description = []
genre=[]
cast=[]
cas=[]
image_url = []

pages = np.arange(1, 50001, 50)

for page in pages:
    print(f"SCRAPPING DATA...{page}/{pages[-1]}")

    page = requests.get("https://www.imdb.com/search/title/?title_type=feature&primary_language=en&start="+str(page)+"&ref_=adv_nxt")
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
    for store in movie_data:
        id = store.h3.a['href'].split('/')[2]
        movie_id.append(id)

        name = store.h3.a.text
        movie_name.append(name)
        
        year_of_release = store.h3.find('span', class_ = "lister-item-year text-muted unbold").text.replace('(', '')
        year_of_release=year_of_release.replace(')','')
        year.append(year_of_release)
        
        runtime = store.p.find("span", class_ = 'runtime').text if store.find('span', class_ = "runtime") else "NA"
        time.append(runtime)
        
        gen_element = store.p.find("span", class_ = 'genre')
        gen = gen_element.text.replace('\n', '') if gen_element else ""
        genre.append(gen)
        
        rate = store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '') if store.find('div', class_ = "inline-block ratings-imdb-rating") else "NA"
        rating.append(rate)
        #rate = store.find('div', class_ = "ratings-bar").find('strong').text.replace('\n', '')
        #rating.append(rate)
        
        meta = store.find('span', class_ = "metascore").text if store.find('span', class_ = "metascore") else "NA"#if meta score not present then *
        
        metascore.append(meta)
        
        #dire=store.find('p',class_ = "metascore")
        # dire=store.find('p',class_='').find_all('a')[0].text
        director_element = store.find('p', class_='').find_all('a')
        dire = director_element[0].text if director_element else ""


        director.append(dire)
        
        #cas=([a.text for a in store.find('p',class_='').find_all('a')[1:]])
        #cast=','.join(map(str,cas))
        cast.append([a.text for a in store.find('p',class_='').find_all('a')[1:]])
      
        value = store.find_all('span', attrs = {'name':'nv'}) if store.find_all('span', attrs = {'name':'nv'}) else 'NA'
        vote = value[0].text if store.find_all('span', attrs = {'name':'nv'}) else ""

        votes.append(vote)
        
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else ""
        description.append(description_)

        image = store.find('img', class_='loadlate')
        image_src = image['loadlate'] if image else ""
        image_url.append(image_src)

for i in cast:
    c=','.join(map(str,i))
    cas.append(c)
   
movie_list = pd.DataFrame({"id":movie_id , "title": movie_name, "year_release" : year, 
                           "duration": time, "genre":genre, "rating": rating, 
                           "metascore": metascore, "director":director, "cast":cas, 
                           "votes" : votes,"description": description, "img_url" : image_url})
movie_list.to_csv("../../data/movie.csv", index=False)