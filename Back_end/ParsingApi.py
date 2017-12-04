
# coding: utf-8


import urllib.request
import requests
import ScrapingApi
import json
# import ConnectDB

class NewsAPI:
    Url = ''
    Author = ''
    Title = ''
    Description = ''
    ImageUrl = ''
    PublishedAt = ''
 
    def __init__(self, url, author, title, description, imageUrl, publishedAt):
        self.Url = url
        self.Author = author
        self.Title = title
        self.Description = description
        self.ImageUrl = imageUrl
        self.PublishedAt = publishedAt
    
def read_list(link):
    for i in range(len(link)):
        get_and_write_data(link[i])
 

def get_and_write_data(link): 
    for i in range(len(link)):
        try:
            response = urllib.request.urlopen(link[i])
            html = response.read().decode()
            data = json.loads(html)
        except ValueError:  
            print ('Decoding JSON has failed')
            continue

        news = data['articles']

        for i in range(len(news)):
            author = news[i]['author']
            title = news[i]['title']
            description = news[i]['description']
            url = news[i]['url']
            image = news[i]['urlToImage']
            publishedAt = news[i]['publishedAt']
        
            newsApi = NewsAPI(url, author, title, description, image, publishedAt)
            # ConnectDB.uploadDBNewsApi(newsApi)

            ScrapingApi.get_news_content(url)

link = [
        "https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=top&apiKey=47236378059c4972a2c99d0d4f58cf61",
        "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe", 
        "https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=independent&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=reuters&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=time&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe"
        ]

get_and_write_data(link)





