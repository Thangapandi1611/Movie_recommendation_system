# -*- coding: utf-8 -*-
"""MovieRecommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yrjyG9q4gXdeUhnQ6Qfutyul9IaATBLg
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

#Function to extract data from imdb for 50 pages
def get_all(url='https://www.imdb.com/list/ls526715737/?sort=list_order,asc&st_dt=&mode=detail&page='):
  actors=[]
  #synapsis
  synapsis=[]
  name=[]
  genre=[]
  year=[]
  ratting=[]
  try:
    page=1

    while page<51:
      get_url=url+str(page)
      response=requests.get(get_url)
      soup=BeautifulSoup(response.content,'lxml')
      mov=soup.findAll('div',class_="lister-item mode-detail")
      movie_data= soup.findAll('div',attrs={'class' : 'lister-item mode-detail'})
      for m in mov:
        actors.append([ a_tag.text for a_tag in m.find('div',class_='lister-item-content').findAll('p',class_='text-muted text-small')[1].findAll('a')])
      rat=soup.findAll('span',attrs={'class': 'ipl-rating-star__rating'})
      c=0
      for i in rat:
        if c%23==0:
          ratting.append(i.text)
        c+=1

      for i in movie_data:
        name.append(i.h3.a.text)
        release=i.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        year.append(release)

      for i in movie_data:
        gen=i.p.find('span',class_='genre').text.replace('\n','')
        genre.append(gen)
      for i in movie_data:
        synapsis.append(i.findAll('p',attrs={'class':''}))
      for i in range(len(synapsis)):
        synapsis[i]=str(synapsis[i]).replace('<p class="">','').replace('</p>','').replace('\n','').replace(']','').replace('[','')
      print(page)
      page+=1

  except Exception as e: print(e)
  return [actors,synapsis,name,genre,year,ratting]

a=get_all()

#Storing Values in List
Name=a[2]
Year=a[4]
Ratng=a[5]
Genre=a[3]
Cast=a[0]
OverView=a[1]

print(Cast)

#Storing Actors and Directors Separately
Actors=[]
Director=[]
for i in range(len(Cast)):
  Actors.append(Cast[i][1:])
  Director.append([Cast[i][0]])

"""print(Name)
print(Year[0])
print(Ratng[0])
print(Cast[0])
print(Genre[0])
print(OverView[0])

"""

data={
    'id':index,
    'Name':Name,
    'Year':Year,
    'Rating':Ratng,
    'Genre':Genre,
    'Actors':Actors,
    'Director':Director,
    'One-line':OverView
}

index=[i for i in range(len(Name))]

Movies_data=pd.DataFrame(data)

Movies_data

Movies_data.head()

#Converting into List
Movies_data['One-line'] = Movies_data['One-line'].apply(lambda x:x.split())
Movies_data['Genre'] = Movies_data['Genre'].apply(lambda x:x.split())

Movies_data['tags']=Movies_data['Director']+Movies_data['Actors']+Movies_data['Genre']+Movies_data['One-line']

Final_data=Movies_data[['id','Name','Year','Rating','tags']]

#Converting list into str
Final_data['tags'] = Final_data['tags'].apply(lambda x: " ".join(x))
Final_data.head()

# Converting to lower case
Final_data['tags'] = Final_data['tags'].apply(lambda x:x.lower())

Final_data.head()

import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def stems(text):
    T = []

    for i in text.split():
        T.append(ps.stem(i))

    return " ".join(T)

Final_data['tags'] = Final_data['tags'].apply(stems)

Final_data.head()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(Final_data['tags']).toarray()

vector.shape

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)

similarity.shape

Final_data.to_csv('Final_data.csv')

Final_data[Final_data['Name'] == 'Citizen Kane'].index[0]

def recommend(movie):
    index = Final_data[Final_data['Name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(Final_data.iloc[i[0]].Name,Final_data.iloc[i[0]].Year,Final_data.iloc[i[0]].Rating)

recommend("It's a Wonderful Life")

import pickle

pickle.dump(Final_data,open('Movie_Recommendation\movie_list.pkl','wb'))
pickle.dump(similarity,open('Movie_Recommendation\similarity.pkl','wb'))