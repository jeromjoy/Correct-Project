import dateutil.parser as parser
import urllib.request
import requests
import json
from bs4 import BeautifulSoup
import time
import traceback
import psycopg2
import datetime
from urllib.parse import urlparse
from celery import Celery
from celery.schedules import crontab

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 3600 seconds.
    sender.add_periodic_task(3600.0, workerTask.s('NEWS_API'), name='news_api')
    sender.add_periodic_task(3600.0, workerTask.s('FAKE_NEWS'), name='fake_news')

@app.task
def workerTask(args):
    
    if(args=='NEWS_API'):
        
        newsApiCall('NEWS_API')
    elif(args=='FAKE_NEWS'):
        
        fakeNewsCall('FAKE_NEWS')





connectionString = "dbname='correctdb' user='postgres' host='localhost' password='ucdcsngl'"


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



def uploadDBNewsApi(newsApi):

    try:

        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()


        # publishedAt = time.mktime(datetime.datetime.strptime(PublishedAt, "%Y-%m-%d").timetuple())

        cur.execute("INSERT INTO NewsFetchedApi (Url, Author, Title, Description, ImageUrl, PublishedAt) VALUES (%s, %s, %s, %s, %s, %s)", (newsApi.Url, newsApi.Author, newsApi.Title, newsApi.Description, newsApi.ImageUrl, newsApi.PublishedAt))
        conn.commit();
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return



def uploadDBNews(news):

    try:        

        # createdDate = time.mktime(datetime.datetime.strptime(CreatedDate, "%d/%m/%Y").timetuple())
        # fetchedDate = time.mktime(datetime.datetime.strptime(FetchedDate, "%d/%m/%Y").timetuple())
        # lastUsed = time.mktime(datetime.datetime.strptime(LastUsed, "%d/%m/%Y").timetuple())
        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()

        cur.execute("INSERT INTO News (Article, Title, Author, OriginalContent, CreatedDate, FetchedDate,ArticleUrl,LastUsed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (news.Article, news.Title, news.Author, news.OriginalContent, news.CreatedDate, news.FetchedDate, news.ArticleUrl, news.LastUsed))
        conn.commit();
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return

def checkUrlInDB(href):
    try:
        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()
        query = "select ArticleUrl from news where ArticleUrl = '" + href+"'"

        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if(len(rows)>0):
            return 0
        else:
            return 1



    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return


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
            uploadDBNewsApi(newsApi)

            get_news_content_api(url)


def newsApiCall(args):
    
    link = ["https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=top&apiKey=47236378059c4972a2c99d0d4f58cf61",
        "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=independent&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=reuters&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe",
        "https://newsapi.org/v1/articles?source=time&sortBy=top&apiKey=b9195c69cd60473bb517fcd8289e6afe"]

    get_and_write_data(link)



def get_news_firstpage(link):
    for i in range(len(link)):
        link[i] = 'http://' + link[i]
        headers = {'user-agent' : 'Mozilla/5.0'}            
        try:
            source = requests.get(link[i], headers = headers)
            soup = BeautifulSoup(source.content, "lxml")
        except requests.exceptions.ConnectionError:
            print ('Connection refused!!!')
        
        
        if (soup.findAll('article')):
            for article in soup.findAll('article'):
                if (article.find('a')):
                    href = article.find('a').get('href')
                    if href.startswith('http'):
                        href = href
                    else:
                        href = link[i] + href
                    get_news_content(href)
                else:
                    print ('not able to get <a>!!')
        else: 
            print ('not able to get <article>!!')


        
def get_news_content(href):


    print("New Data\n\n\n\n\n\n",href)
    if(checkUrlInDB(href)==0):
        print("Link already in DB")
        return

    headers = {'user-agent' : 'Mozilla/5.0'}
    title = None
    article = None
    author = None
    orginalContent = None
    createdDate = None
    date= None
    
    try:
        source = requests.get(href, headers = headers)
    except requests.exceptions.ConnectionError:
        source.status_code = "Connection refused"
    if (BeautifulSoup(source.content, "lxml").body):

        soup = BeautifulSoup(source.content, "lxml").body
        
       
        if (soup.findAll('p')):            
            article = []
            for paragraph in soup.findAll('p'):
                article.append(paragraph.text)
        else:
            article = 'Unknown'


            
        
        
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        fetchedDate = date
        lastUsed = date
        orginalContent = source.content
        
        
        if (urlparse(href).netloc == 'americannews.com'):              
            if (soup.findAll('h1')):
                for title in soup.findAll('h1'):
                    title = title.text
            else:
                title = 'Unknown'
            
            if (soup.find('time',{'class': 'rpwe-time published'})):
                createdDate = soup.find('time',{'class': 'rpwe-time published'}).text

                createdDate = (parser.parse(createdDate)).isoformat()
            else: 
                createdDate = None
            
            if (soup.findAll('b')):
                for author in soup.findAll('b'):
                    author = author.text
            else:
                author = 'Unknown'
                    
         

        elif (urlparse(href).netloc == 'www.activistpost.com'):
            if (soup.findAll('span', {'class': 'entry-meta-date updated'})):
                for createdDate in soup.findAll('span', {'class': 'entry-meta-date updated'}):
                    createdDate = (parser.parse(createdDate.text)).isoformat()
            else:
                createdDate = None

            if (soup.findAll('h1', {'class': 'entry-title'})):
                for title in soup.findAll('h1', {'class': 'entry-title'}):
                    title = title.text
            else:
                title = 'Unknown'
            for authors in soup.findAll('p'):
                if (authors.findAll('a')):
                    for author in authors.findAll('a'):
                        author = author.text
                else: 
                    author = 'Unknown'
        
        
        
        elif (urlparse(href).netloc == 'www.thedailysheeple.com'):
            if (soup.findAll('time', {'class': 'entry-date'})):
                for createdDate in soup.findAll('time', {'class': 'entry-date'}):
                    createdDate = (parser.parse(createdDate.text)).isoformat()
            else:
                createdDate = None
            if (soup.findAll('h1', {'class': 'entry-title'})):
                for title in soup.findAll('h1', {'class': 'entry-title'}):
                    title = title.text
            else:
                title = 'Unknown'
            if (soup.findAll('span', {'class': 'author vcard'})):
                for author in soup.findAll('span', {'class': 'author vcard'}):
                    author = author.text
            else: 
                author = 'Unknown'
            
        
        
        elif (urlparse(href).netloc == 'waterfordwhispersnews.com'):
            if (soup.findAll('p', {'class': 'byline byline-left '})):
                for createdDate in soup.findAll('p', {'class': 'byline byline-left '}):
                    createdDate = None
            else:
                createdDate = None
            if (soup.findAll('h1', {'class': 'entry-title'})):
                for title in soup.findAll('h1', {'class': 'entry-title'}):
                    title = title.text
            else:
                title = 'Unknown'
            
            if (soup.findAll('span', {'class': 'author vcard'})):
                for author in soup.findAll('span', {'class': 'author vcard'}):
                    author = author.text
            else: 
                author = 'Unknown'

        
        
        elif (urlparse(href).netloc == 'www.clickhole.com'):
            if (soup.findAll('div', {'class': 'pub_date'})):
                for createdDate in soup.findAll('div', {'class': 'pub_date'}):
                    createdDate = (parser.parse(createdDate.text)).isoformat()
            else:
                createdDate = None
            
            if (soup.findAll('h1', {'class': 'headline'})):
                for title in soup.findAll('h1', {'class': 'headline'}):
                    title = title.text
            else:
                title = 'Unknown'
            if (soup.findAll('span', {'class': 'author vcard'})):
                for author in soup.findAll('span', {'class': 'author vcard'}):
                    author = author.text
            else: 
                author = 'Unknown'
           
        

        elif (urlparse(href).netloc == 'theonion.com'):
            if (soup.findAll('span', {'class': 'content-published-mobile'})):
                for createdDate in soup.findAll('span', {'class': 'content-published-mobile'}):
                    createdDate = (parser.parse(createdDate.text)).isoformat()
            else:
                createdDate = None

            if (soup.findAll('header', {'class': 'content-header'})):
                for title in soup.findAll('header', {'class': 'content-header'}):
                    title = title.text
            else:
                title = 'Unknown'

            if (soup.findAll('span', {'class': 'author vcard'})):
                for author in soup.findAll('span', {'class': 'author vcard'}):
                    author = author.text
            else: 
                author = 'Unknown'

        else:
            title = 'Unknown'
            author = 'Unknown'
            createdDate = None
    else:
        print ('can not get connent')
        return
    news = News(article, title, author, orginalContent, createdDate, date, href, date)
    uploadDBNews(news)    



def fakeNewsCall(args):
    
    link = [
            'americannews.com',
            'thedailysheeple.com',
            'theonion.com',
            'clickhole.com',
            'activistpost.com'
            'waterfordwhispersnews.com'
            ]


    get_news_firstpage(link)

    


def get_news_content_api(href):
    print("New Data\n\n\n\n\n\n",href)
    if(checkUrlInDB(href)==0):
        print("Link already in DB")
        return
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
         
            if (soup.find('span', {'class':'metadata_byline_author'})):
                for author in soup.find('span', {'class':'metadata_byline_author'}):
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

    news = News(article, title, author, orginalContent, createdDate, date, href, date)
    uploadDBNews(news) 

    

# fakeNewsCall('FAKE_NEWS')
#newsApiCall('NEWS_API')