
import dateutil.parser as parser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
# import ConnectDB

class News:
    Article = ''
    Title = ''
    Author = ''
    OriginalContent = ''
    CreatedDate = ''
    FetchedDate = ''
    ArticleUrl = ''
    LastUsed = ''

    def __init__(self, article , title, author, originalcontent, createddate, fetcheddate, articleurl, lastused):
        self.Article = article
        self.Title = title
        self.OriginalContent = originalcontent
        self.CreatedDate = createddate
        self.FetchedDate = fetcheddate
        self.ArticleUrl = articleurl
        self.LastUsed = lastused
        self.Author = author


def get_news_content(href):
    headers = {'user-agent' : 'Mozilla/5.0'}
    try:
        source = requests.get(href, headers = headers)
    except requests.exceptions.ConnectionError:
        source.status_code = "Connection refused"
    if source.status_code == 200: 
        soup = BeautifulSoup(source.content, "lxml").body       
 
        print (href)
        
        if (soup.findAll('p')):
            for article in soup.findAll('p'):
                article = article.text
        else:
            article = 'Unknown'
          
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        fetchedDate = date
        lastUsed = date
        orginalContent = source.content
         
        if (soup.findAll('h1')):
            for title in soup.findAll('h1'):
                title = title.text
        else:
            title = 'Unknown'
         



        if (urlparse(href).netloc) == 'www.theguardian.com':
            try:
                for createdDate in soup.findAll('time',{'itemprop': 'datePublished'}):
                    ccreatedDate = (parser.parse(createdDate.text)).isoformat()
            except:
                createdDate = None
            
            if(soup.findAll('a', {'class':'tone-colour'})):
                for author in soup.findAll('a', {'class':'tone-colour'}):
                    author = author.text
            else:
                author = 'Unknown'
 



        elif (urlparse(href).netloc) == 'www.bbc.co.uk':
            if (soup.find('div', {'class': 'date date--v2'})):
                for createdDate in soup.findAll('div', {'class': 'date date--v2'}):
                    createdDate = (parser.parse(createdDate.text)).isoformat()
            else: 
                createdDate = None

            if (soup.findAll('a', {'class':'tone-colour'})):
                for author in soup.findAll('a', {'class':'tone-colour'}):
                    author = author.text
            else:
                author = 'Unknown'



        elif (urlparse(href).netloc) == 'www.abc.net.au':
            if (soup.findAll('span', {'class': 'print'})):
                for createdDate in soup.findAll('span', {'class': 'print'}):
                    if (createdDate):
                        createdDate = (parser.parse(createdDate.text)).isoformat()
                    else:
                        createdDate = None
            else:
                createdDate = None
           
            if (soup.find('a', {'target':'_self'})):
                author = soup.find('a', {'target':'_self'}).text
            else:
                author = 'Unknown'



           
        elif (urlparse(href).netloc) == 'www.cnn.com':
           
            try:
                createdDate = soup.find('p', {'class': 'update-time'})
                createdDate = (parser.parse(createdDate.text)).isoformat()
            except:
                createdDate = None
         
            if (soup.find('span', {'class':'metadata__byline__author'})):
                for author in soup.find('span', {'class':'metadata__byline__author'}):
                    author = author.string
            else:
                author = 'Unknown'



           
        elif (urlparse(href).netloc) == 'www.independent.co.uk':
           
            try:
                createdDate = soup.find('time')
                createdDate = (parser.parse(createdDate.text)).isoformat()
            except:
                createdDate = None
            
            if (soup.find('span', {'itemprop':'name'})):
                for author in soup.find('span', {'itemprop':'name'}):
                    author = author.string
            else:
                author = 'Unknown'


            
        elif (urlparse(href).netloc) == 'www.reuters.com':
            
            try:
                createdDate = soup.find('span', {'class': 'timestamp'})
                createdDate = parser.parse(createdDate.text)
            except:
                createdDate = None
           
            if (soup.find('span', {'class':'author'})):
                for author in soup.find('span', {'class':'author'}):
                    author = author.string
            else: 
                author = 'Unknown'



           
        elif (urlparse(href).netloc) == 'time.com':

            try:
                createdDate = soup.find('div', {'class': 'row text font-accent size-1x-small color-darker-gray'})
                createdDate = (parser.parse(createdDate.text)).isoformat()
            except: 
                createdDate = None
            
            if (soup.find('a', {'class':'text font-accent color-brand size-1x-small _1HynphR0'})):
                for author in soup.find('a', {'class':'text font-accent color-brand size-1x-small _1HynphR0'}):
                    author = author.string
            else: 
                author = 'Unknown'
            
        else:
            createdDate = None
            author = 'Unknown'


    else:
        print ('can not get connent')
        return 
    # print (createdDate)

    # news = News(title, article, author, orginalContent, createdDate, date, href, date)
    # ConnectDB.uploadDBNews(news)




