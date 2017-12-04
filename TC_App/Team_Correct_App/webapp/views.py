from django.http import HttpResponseRedirect
from django.http import HttpResponse

# package that collects several modules for working with URLs:
# https://docs.python.org/3/library/urllib.html
from urllib.parse import urlparse

# Models classes for objects
from webapp.models import News,NewsApi,NotFoundNewsApi,NewsArticle

# Time access and conversions
# https://docs.python.org/3/library/time.html?highlight=time#module-time
import time

# Handle error
from webapp.errorTrace import handleErrorTracePsyco,handleErrorTrace

#python parser for human readable dates 
# https://github.com/scrapinghub/dateparser
import dateparser


# Service functions
from webapp.services import getData,smart_truncate,addScore, errorHandle, uploadDBNews, convertToContent, collectDataSet



# jsonData collected from 
#   https://raw.githubusercontent.com/bs-detector/bs-detector/dev/ext/data/data.json   
#   - http://guides.library.harvard.edu/fake
#   B.S. Detector searches all links on a given webpage for references to unreliable sources, checking against a manually compiled list of domains.
# 
#   
#   https://raw.githubusercontent.com/BigMcLargeHuge/opensources/master/sources/sources.json
#   - http://www.opensources.co/
#   OpenSources is a curated resource for assessing online information sources, available for public use. Websites in this resource range
#   from credible news sources to misleading and outright fake websites
# 
from webapp.jsonResource import jsonData

# Combines a given template with a given context dictionary and returns an HttpResponse object
from django.shortcuts import render

from webapp.classList import class_list_title, class_list_paragraph, class_list_author, class_list_date

# HTTP library for Python
import requests

# https://www.crummy.com/software/BeautifulSoup/
# Beautiful Soup is a Python library designed for screen scraping
from bs4 import BeautifulSoup

# dateutil - powerful extensions to datetime
# https://dateutil.readthedocs.io/en/stable/
import dateutil.parser as parser

# re — Regular expression operations
# https://docs.python.org/3/library/re.html
import re

# json — JSON encoder and decoder
# https://docs.python.org/3/library/json.html
import json








# Home page of the application
def index(request):
    if request.method == 'POST':

        url = request.POST.get('url','')
        # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
        regex = re.compile(
                r'^((?:http|ftp)s?://)*' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if (regex.match(url)):
            # scrap the article if url valid
            onError = scraping(url,request)
            # Navigate to error handle
            if(onError):
                return onError
            else:
                #  Collect DataSet and ScoreArticle if scrapping was successfull
                collectDataSetAndScoreArticle(url)

        else:
            return errorHandle(request,"There was an error reaching the site. Make sure the URL is valid.")
            
        
        # On success of collectDataSetAndScoreArticle navigate to search url to display result.
        return HttpResponseRedirect("/search/?search="+url)
            
    return render(request, 'webapp/home.html')


                

# Api to get result in modular way
def searchApi(request):
    t = request.GET.get('checkurl', 'Not found')
    News= getData(t)
    if(News == None):
        newsApi = NotFoundNewsApi()
    else:
        newsApi = NewsApi(News.title,News.author,str(News.createddate));
        
        if(News.category and News.category.score):
            newsApi.categoryScore =  int(News.category.score/2)
        if(News.grammar):
            newsApi.grammarScore = News.grammar.score
        if(News.wordcount):
            newsApi.wordcountScore = News.wordcount.score
        if(News.authorScore):
            newsApi.authorScore = News.authorScore.score
        if(News.datecheck):
            newsApi.datecheckScore = int(News.datecheck.score/2)
        if(News.subUrl):
            newsApi.subUrlScore = News.subUrl.score
        if(News.totalScore):
            newsApi.totalScore = News.totalScore.score
            newsApi.description = News.totalScore.description

    data = json.dumps(newsApi.__dict__)
    return HttpResponse(data, content_type='application/json')


#  Search page to display the result of score
def search(request):
    t = request.GET.get('search', 'Not found')
    News= getData(t)
    if (News == None):
        return render(request, 'webapp/None.html')
    return render(request, 'webapp/temp.html', {'News':News})





articleContentList = []

# 
# Scrapping function to get the content of the artcle and scrap the article
# 
# 
        
def scraping(href,request):
    
    print(href)
    headers = {'user-agent' : 'Mozilla/5.0'}
    try:
        source = requests.get(href, headers = headers)
        if (BeautifulSoup(source.content, "lxml")):
            soup = BeautifulSoup(source.content, "lxml").body 
            news = NewsArticle(None, None, None, None, None, None, None, None)
            date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            news.FetchedDate = date
            news.LastUsed = date 
            news.ArticleUrl = href
            content = soup
            
            scrape_details(content,news)
            
            if(news.Article ==None or news.Title == None):
                
                
                print("Unsuccessfull scraping")
                return errorHandle(request,"The site was unable to fetch data successfully.")
            else:
                
                uploadDBNews(news)
            
        else:
            print ('can not get the information!')
            return errorHandle(request,"Unable to get the required information!")
    except:
        print ('can not connect to the web page!')
        return errorHandle(request,"Unable to connect to the web page!")
            




SubUrl_list = []


# 
# Scrapping function to scrap the news content based on the class list for article, title, date and urls
# 
# 

def scrape_details(content,news):
    print("scrape_details call") 
    print(len(content))           
    news.content = content

    
    for i in range(len(class_list_title)):
        if (content.find('',{'class':class_list_title[i]})):
#             print (class_list_title[i])
            news.Title = content.find('',{'class':class_list_title[i]}).text         
            break
        else:
            news.Title = None

    

    del articleContentList[:]
    del SubUrl_list[:]
    news.Article = []
    # SubUrl_list = []
    
    for i in range(len(class_list_paragraph)):
        if (content.find('',{'class': class_list_paragraph[i]})): 
#             print (class_list_paragraph[i])
            paragraphs = content.find('',{'class': class_list_paragraph[i]})
            if (paragraphs.findAll('p')):
                for paragraph in paragraphs.findAll('p'):
                    news.Article.append(paragraph.text)
                    articleContentList.append(paragraph.text)
                    try:
                        if(paragraph.find('', href=True)):
                            subURL = paragraph.find('', href=True)['href']
                            if (subURL):
                                surl=urlparse(subURL).netloc
                                if(surl.startswith('www.')):
                                    surl = surl.replace("www.","")
                                print(subURL)
                                print(surl)
                                try:
                                    if(surl != None and surl !="" and jsonData[surl] != None):
                                        print(len(SubUrl_list))
                                        SubUrl_list.append(subURL)
                                except:
                                    print("No key found")
                                    handleErrorTrace()
                    except:
                        print("Sub url error in paragrapg")
                break
        else:    
            news.Article = []
            
            
            


    
    for i in range(len(class_list_author)):
        if (content.find('',{'class': class_list_author[i]})):
#             print (class_list_author[i])
            news.Author = content.find("",{'class':class_list_author[i]}).text 
            break
        else:
            news.Author = None


    

    for i in range(len(class_list_date)):
        if (content.find('',{'class': class_list_date[i]})):
#             print(class_list_date[i])
            news.createdDate = content.find('',{'class': class_list_date[i]})
            print("\nCreted date\n")
            print (news.createdDate.text)
            # try:
            #     news.createdDate = (dateparser.parse(news.createdDate.text)).isoformat()
            # except:
            #     news.createdDate = None


            try:
                news.CreatedDate = (parser.parse(news.createdDate['datetime'])).isoformat()
            except:
                try:
                    news.CreatedDate = (parser.parse(news.createdDate.text)).isoformat()
                except:
                    try:
                        news.CreatedDate = (dateparser.parse(news.createdDate.text)).isoformat()
                    except:
                        news.CreatedDate = None
            print("\nCreated date\n")
            print (news.CreatedDate)
            break
        else:
            news.createdDate = None

    return

# 
# Collect dataset for all the features and evaluate score for the article
# 
# 

def collectDataSetAndScoreArticle(url):

    
    
        tempnewsid = collectDataSet(url,articleContentList,int(len(SubUrl_list)))
        print("News ID\n\n" + str(tempnewsid))
        if(tempnewsid):
            addScore(tempnewsid)

    




