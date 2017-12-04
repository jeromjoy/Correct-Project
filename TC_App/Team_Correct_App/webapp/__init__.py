from django.shortcuts import render
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db import connection
import psycopg2
import math
from urllib.parse import urlparse
#from django.db import models
from webapp.models import News

import time
import traceback
import psycopg2
import datetime
from urllib.parse import urlparse
from celery import Celery
from celery.schedules import crontab
from django.core import serializers

import ast
import dateparser




from django.shortcuts import render




from django.template import Context, loader

from webapp.models import URL

import re
SubUrl_list = []

import json
jsonData = None
# jsonData  = json.load(open('/static/data.json'))

# subURLCount = 0
# print("subURLCount" + str(subURLCount))

class News :
    article = None
    title = None
    author = None
    # scoredomain = None
    createddate = None
    # fetcheddate = None
    articleurl = None
    category = None
    # domaintype = None

    def __init__(self,title, article, author,createddate, articleurl):
        self.article = article
        self.title = title
        self.author = author
        # self.scoredomain = scoredomain
        self.createddate = createddate
        # self.fetcheddate = fetcheddate
        self.articleurl = articleurl
        # self.domaintype = domaintype

class Domain:
    title = None
    score = None
    style = None
    def __init__(self, score,title):
        self.title = title
        self.score = score
        self.viewscore = int(score/2)
        if(score<4):
            self.style="red"
        elif (score<8):
            self.style="yellow"
        else:    
            self.style = "blue"
class WordCount:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"  

class DateCheck:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        self.viewscore = int(score/2)
        if(score<4):
            self.style="red"
        elif (score<8):
            self.style="yellow"
        else:    
            self.style = "blue"  

class Author:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        if(score<3):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"  

class Grammar:
    score = None
    percentScore = None
    style = None
    def __init__(self, score,percentScore):
        self.score = score
        self.percentScore = percentScore
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"
class SubUrl:
    score = None
    style = None
    def __init__(self, score):
        self.score = score
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"

class TotalScore:
    score = None
    style = None
    description = None
    def __init__(self, score, description):
        if(score<30):
            self.style="red"
        elif (score<80):
            self.style="yellow"
        else:    
            self.style = "blue"
        self.score = score
        self.description = description

def upload(request):
    return render(request, 'webapp/upload.html')



# def get(self, request):
#     form = HomeForm()
#     return render[request. self.template_name, {'form': form}]

# def post(self, request):
#     form = HomeForm(request.POST)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.user = request.user
#         post.save()
#
#         text = form.cleaned_data['post']
#         form = HomeForm()
#         return redirect('webapp:home')
#
#         args = {'form': form, 'text': text}
#         return render(request, self.template_name, args)


# 
# https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
# 

articleContentList = []
def index(request):
    if request.method == 'POST':

        # form = CostForm(request.POST)

        # if form.is_valid():

            url = request.POST.get('url','')

            

            # regex = re.compile("[-a-zA-Z0-9@:%.\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%\+.~#?&//=]*)")

            regex = re.compile(
                    r'^((?:http|ftp)s?://)*' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if (regex.match(url)):
                print('correct')
                # link = 'http://www.thedailysheeple.com/astronomers-detect-strange-radio-signals-from-nearby-star_072017'
                # link = 'http://americannews.com/hollywood-liberal-alyssa-milano-throws-rocks-trump-hits-hillary-obama-instead/'
                
                response = scraping(url,request)
                if(response):
                    return response
                
                newcall(url)
                # return redirect('search/?search='+url)

            else:
                return errorHandle(request,"There was an error reaching the site. Make sure the URL is valid.")
                
            
            return HttpResponseRedirect("/search/?search="+url)
            # template = loader.get_template("webapp/home.html")
            # return HttpResponse(template.render())

    

    return render(request, 'webapp/home.html')


def errorHandle(request,errorText="Site is facing some issues."):
    form = errorText
    print('error')
    return render(request, 'webapp/home.html',{'form': form})
                



def smart_truncate(content, length=250, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

# getData(url):
# return value
#         return render(request, 'webapp/upload.html', {'p':p})


class Domain:
    title = None
    score = None
    style = None
    def __init__(self, score,title):
        self.title = title
        self.score = score
        self.viewscore = int(score/2)
        if(score<4):
            self.style="red"
        elif (score<8):
            self.style="yellow"
        else:    
            self.style = "blue"
class WordCount:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"  

class DateCheck:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        self.viewscore = int(score/2)
        if(score<4):
            self.style="red"
        elif (score<8):
            self.style="yellow"
        else:    
            self.style = "blue"  

class Author:
    
    score = None
    style = None
    def __init__(self, score):
        
        self.score = score
        if(score<3):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"  

class Grammar:
    score = None
    percentScore = None
    style = None
    def __init__(self, score,percentScore):
        self.score = score
        self.percentScore = percentScore
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"
class SubUrl:
    score = None
    style = None
    def __init__(self, score):
        self.score = score
        if(score<2):
            self.style="red"
        elif (score<4):
            self.style="yellow"
        else:    
            self.style = "blue"

class TotalScore:
    score = None
    style = None
    description = None
    def __init__(self, score, description):
        if(score<30):
            self.style="red"
        elif (score<80):
            self.style="yellow"
        else:    
            self.style = "blue"
        self.score = score
        self.description = description






class NewsApi :
    
    title = None
    author = None
    
    createddate = None
    
    
    totalScore = None
    subUrlScore = None
    grammarScore = None
    authorScore = None
    datecheckScore = None
    wordcountScore = None
    categoryScore = None
    # domaintype = None

    def __init__(self,title, author,createddate):
        
        self.title = title
        self.author = author
        self.createddate = createddate

class NotFoundNewsApi:
    data = None
    def __init__(self):
        
        self.data = "None"
        

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
    # if (News == None):
        
    
    # foos = News.objects.all()
    # data = serializers.serialize('json', News)
    # data = serializers.serialize('json', {name:"Jerom"})
    data = json.dumps(newsApi.__dict__)
    return HttpResponse(data, content_type='application/json')



def search(request):
    t = request.GET.get('search', 'Not found')
    News= getData(t)
    if (News == None):
        return render(request, 'webapp/None - Copy.html')
    return render(request, 'webapp/temp.html', {'News':News})

    #return HttpResponse(text+text2, {'News':News})




def getData (value):
        #conn=psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='Correct server' user='postgres' password='ucdcsngl⁠⁠⁠⁠'")
        cursor = connection.cursor()
        parsed_uri = urlparse(value)
        domain = parsed_uri.netloc
        if(domain.startswith('www.')):
                domain = domain.replace("www.","")
        #cursor.execute('SELECT articleurl,s.score FROM news,domainfilterlist d,domaintypescore s where articleurl=%s', [domain])
        # query = "SELECT  n.title, n.article, n.author, n.createddate, n.fetcheddate, n.articleurl, s.score, d.domaintype FROM news n,domainfilterlist d,domaintypescore s where articleurl= '"+ value +"' and d.url ='"+ domain + "' and s.type = d.domaintype order by s.score asc";
        newsQuery = "SELECT  title, article, author, createddate, articleurl,newsid  FROM news where articleurl= '"+ value +"'";
        
        #cursor.execute('SELECT articleurl,s.score FROM news,domainfilterlist d,domaintypescore s where articleurl=%s', [domain])
        cursor.execute(newsQuery)
        # News="hello"
        newsRow = cursor.fetchone() # fetchall() may not be the right call here?
        # for row in rows:
        if (newsRow == None ):
            return None
        print(newsRow[2])
        contentArticle=newsRow[1].strip()
        contentArticle = contentArticle.replace("'","")
        contentArticle = contentArticle.replace("\"","")
        contentArticle = contentArticle.replace('{', '')
        contentArticle = contentArticle.replace('}', '')
        contentArticle = contentArticle.replace('%', '')
        contentArticle = contentArticle.replace(',', '')
        contentArticle = contentArticle.replace('\r', '').replace('\n', '')
        contentArticle = re.sub(r'[?|$|!]',r'',contentArticle)
        
        data =  News(newsRow[0],smart_truncate(contentArticle),newsRow[2],newsRow[3],newsRow[4])
        newsID = newsRow[5]

        domainQuery = "SELECT  s.score, d.domaintype FROM domainfilterlist d,domaintypescore s where d.url ='"+ domain + "' and s.type = d.domaintype order by s.score asc";
        # print(domainQuery)
        cursor.execute(domainQuery)
        # News="hello"
        domainRow = cursor.fetchone() # fetchall() may not be the right call here?
        # for row in rows:
        if (domainRow == None ):
            data.category = None
        else:
            data.category =  Domain(domainRow[0],domainRow[1])


        grammerDataQuery = "SELECT  grammarscore FROM datasetnewsscore where newsid="+str(newsID);

        cursor.execute(grammerDataQuery)
        # News="hello"
        grammarDataRow = cursor.fetchone() # fetchall() may not be the right call here?
        # for row in rows:
        
        # print(grammarDataRow)

        scoreQuery = "SELECT  grammar,wordcount,datecheck,author,subdomain FROM score where newsid="+str(newsID);

        cursor.execute(scoreQuery)
        # News="hello"
        scoreRow = cursor.fetchone() # fetchall() may not be the right call here?
        # for row in rows:
        # print(scoreRow)
        if (scoreRow == None or scoreRow[0]==None or grammarDataRow == None):
            data.grammar = None
        else:
            data.grammar =  Grammar(scoreRow[0],grammarDataRow[0])
        if (scoreRow == None or scoreRow[1]==None ):
            data.wordcount = None
        else:
            data.wordcount =  WordCount(scoreRow[1])
        if (scoreRow == None or scoreRow[2]==None ):
            data.datecheck = None
        else:
            data.datecheck =  DateCheck(scoreRow[2])
        if (scoreRow == None or scoreRow[3]==None ):
            data.authorScore = None
        else:
            data.authorScore =  Author(scoreRow[3])
        if (scoreRow == None or scoreRow[4]==None ):
            data.subUrl = None
        else:
            data.subUrl =  SubUrl(scoreRow[4])
        
        totalScore=0

        # if(data.category and data.category.score):
        #     totalScore = 3* data.category.score
        #     if(data.grammar):
        #         totalScore += data.grammar.score
        #     if(data.wordcount):
        #         totalScore += data.wordcount.score
        #     if(data.authorScore):
        #         totalScore += 2*data.wordcount.score
        #     if(data.datecheck):
        #         totalScore += data.datecheck.score
        #     if(data.subUrl):
        #         totalScore += data.subUrl.score
        # else:

        #     if(data.grammar):
        #         totalScore += data.grammar.score
        #     if(data.wordcount):
        #         totalScore += data.wordcount.score
        #     if(data.authorScore):
        #         totalScore += 2*data.wordcount.score
        #     if(data.datecheck):
        #         totalScore += data.datecheck.score
        #     if(data.subUrl):
        #         totalScore += data.subUrl.score

        if(data.category and data.category.score):
            totalScore =  2 * data.category.score
            if(data.grammar):
                totalScore += data.grammar.score
            if(data.wordcount):
                totalScore += data.wordcount.score
            if(data.authorScore):
                totalScore += data.authorScore.score
            if(data.datecheck):
                totalScore += data.datecheck.score
            if(data.subUrl):
                totalScore += data.subUrl.score
            totalScore = int((totalScore*100)/50)
        else:

            if(data.grammar):
                totalScore += data.grammar.score
            if(data.wordcount):
                totalScore += data.wordcount.score
            if(data.authorScore):
                totalScore += data.authorScore.score
            if(data.datecheck):
                totalScore += data.datecheck.score
            if(data.subUrl):
                totalScore += data.subUrl.score
            totalScore = int((totalScore*100)/30)
        
        
        descriptionScore = ""
        if(totalScore<30):
            descriptionScore = "The article is fake"
        elif (totalScore<70):
            descriptionScore = "The article probably is fake"
        elif (totalScore<95):
            descriptionScore = "The article probably is Real"
        elif(totalScore<=100):
            descriptionScore = "The article is Real"
        else:
            descriptionScore = "Unable to calculate score"
        data.totalScore = TotalScore(totalScore,descriptionScore)
        return data








# Fairy
import requests
from bs4 import BeautifulSoup
import dateutil.parser as parser
import time

class NewsArticle:
    Article = ''
    Title = ''
    Author = ''
    OriginalContent = ''
    CreatedDate = ''
    FetchedDate = ''
    ArticleUrl = ''
    LastUsed = ''
    
    
    def __init__(self, article , title , author , originalcontent , createddate , fetcheddate , articleurl , lastused ):
        self.Article = article
        self.Title = title
        self.OriginalContent = originalcontent
        self.CreatedDate = createddate
        self.FetchedDate = fetcheddate
        self.ArticleUrl = articleurl
        self.LastUsed = lastused
        self.Author = author
        
        
def scraping(href,request):
    articleContentList = []
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
                
                try:
                    print("\n\\nNews article\n\n"+news.Article)
                    print("\n\\nNews title\n\n"+news.Title)
                except:
                    print("Error unable to get all")
                print("Unsuccessfull scraping")
                return errorHandle(request,"The site was unable to fetch data successfully.")
            else:
                # subURLCount = len(SubUrl_list)    
                # print("\n\n\n\n\n\n\nSub url count"+str(subURLCount)+"\n\n\n\n\n\n\n\n\n")
                uploadDBNews(news)
            
        else:
            print ('can not get the information!')
            return errorHandle(request,"Unable to get the required information!")
    except:
        print ('can not connect to the web page!')
        return errorHandle(request,"Unable to connect to the web page!")
            
          


                
              



connectionString = "dbname='correctdb' user='postgres' host='localhost' password='ucdcsngl'"

def uploadDBNews(news):

    try:        
        
        
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

def scrape_details(content,news):
    print("scrape_details call") 
    print(len(content))           
    news.content = content
    class_list_title = [
                'title',
                'ArticleHeader_headline_2zdFM',
                'articleheader',
                'article-header',
                'article-title',
                'ArticleHeader__hed___GPB7e',
                'article__headline',
                'entry-title',
                'entry-title single-title',
                'col-lg-9 col-md-8',
                'content__headline',
                'name post-title entry-title',
                'articleTitle',
                'artTitle',
                'blog-title',
                'b-item__title',
                'postarea',
                'full-page-article left-col',
                'headline',
                'post_title',
                'post-title',
                'post-title entry-title',
                'post-headline',
                'pg-headline',
                'page-header',
                'content-header ',
                'field-subhead',
                '_8UFs4BVE',
                'the-title',
                'single-title',
                'single-entry-title',
                'story-title',
                'story-body__h1',
                'xxlarge',
                'row',
                'lede-text-only__hed',
                'asset-headline speakable-headline'
            ] 
    for i in range(len(class_list_title)):
        if (content.find('',{'class':class_list_title[i]})):
#             print (class_list_title[i])
            news.Title = content.find('',{'class':class_list_title[i]}).text         
            break
        else:
            news.Title = None

    class_list_paragraph = [
                'ArticleBody__articleBody___1GSGP',
                'art-postcontent',
                'articles2',
                'article-inner',
                'article-text',                    
                'article-content',
                'article-copy',
                'article_body',
                'article section',
                'articleContentData',
                'article',
                'ArticleBody_body_2ECha',
                'b-item__description',
                'blog-content clearfix',
                'blog-content',
                'body-copy',
                'content-main',
                'content-text', 
                'cb-entry-content clearfix',
                'content__article-body from-content-api js-article__body',
                'content',
                'entry-content clearfix',
                'entry-content full-content',
                'entry clearfix',        
                'entry-content', 
                'entry_content',
                'entry-content print-only',
                'entry-body',
                'entry',                                       
                'entry entry-content',
                'event-text',
                'entry-meta',
                'entry-content-text',
                'field-item even',
                'field-items',
                'field-body',
                'infopage-news',
                'inner-post-entry',
                'td-post-content', 
                'the-content cf',
                'thecontent',
                'text-wrapper',
                'td-post-content td-pb-padding-side',
                'ntText',  
                'new_block',
                'post-single',                     
                'post-content entry-content cf',   
                'post-body entry-content',        
                'post_entry',
                'post_content',
                'post-body',
                'post-content clearfix', 
                'post-bodycopy clearfix',
                'post-single-content box mark-links',
                'post-content',
                'post-9141 post type-post status-publish format-standard has-post-thumbnail hentry category-world tag-fake-news tag-featured tag-satire',
                'vw-post-content clearfix',
                'wpb_wrapper',
                'single-box clearfix entry-content',
                'story-body story-body-1',
                'story-content',
                'story-body__inner',
                'sqs-block-content',
                'single single-post postid-193191 single-format-standard',
                'left relative',
                'l-container',
                'metadata__byline__author',
                'mainContent',
                'mk-single-content clearfix',
                'mvp-post-content-in',
                'group-container ',
                'group-container last',
                'el__leafmedia el__leafmedia--sourced-paragraph',
                'asset-double-wide double-wide p402_premium'
    ]

    print("clear article")
    # del news.Article[:]
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
                                    print(traceback.format_exc())
                    except:
                        print("Sub url error in paragrapg")
                break
        else:    
            news.Article = []
            
            
            


    class_list_author = [
                'postmetadata',
                'author-article-link',
                'author-section',
                'ArticleHeader_byline_1VRIx',
                'article__author-name',
                'field-author',
                'field-items',
                'fn',
                'name',
                'url fn n',
                'author vcard',
                'author left-edge',
                'author has-bio',
                'author',
                'artAuthor',
                'post-author',
                'post_author',
                'meta pf-author',
                'meta-author',
                'meta-holder',
                'mk-author-name',
                'author-name vcard fn',
                'text font-accent color-brand size-1x-small _1HynphR0',
                'theauthor',
                'byline-author',
                'byline__name',
                'byline',
                'blog-author',
                'createdby',
                'cb-author',
                'username',
                'single-author',
                'small',
                'entry-author-name',
                'metadata__byline__author',
                'asset-metabar-author asset-metabar-item'
    ]
    for i in range(len(class_list_author)):
        if (content.find('',{'class': class_list_author[i]})):
#             print (class_list_author[i])
            news.Author = content.find("",{'class':class_list_author[i]}).text 
            break
        else:
            news.Author = None


    class_list_date = [
                'timestamp',
                'entry-date published',
                'entry-date published updated',
                'content-published-mobile',
                'entry-date',
                'entry-meta',
                'entry-meta-content',
                'entry-meta-date updated',
                'byline byline-left ',
                'bydate',
                'blog-date',
                'b-item__asked-by-time',
                'pub_date',
                'post-date',
                'post_date',
                'post-date updated',               
                'time',
                'published', 
                'article-details',
                'article-timestamp',
                'art-postheadericons art-metadata-icons',
                'article_date',
                'ArticleHeader_date_V9eGk',
                'ArticleTimestamp__timestamp___1klks',
                'artData',
                'cb-date',
                'field-post-date',
                'fa fa-clock-o',
                'update-time',
                'row text font-accent size-1x-small color-darker-gray',
                'dateline',
                'datestamp',
                'date',
                'dt-published date-callout',
                'content__dateline-lm js-lm u-h',
                'grDate',
                'submitted',
                'single-date',
                'mk-publish-date',
                'relative ',
                'asset-metabar-time asset-metabar-item nobyline',
                'article__updated',
                'date no-author',
    ]

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

import requests
from pprint import pprint
import psycopg2
import re
from urllib.parse import urlparse

def newcall(url):
    try:
        conn=psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='correctdb' user='postgres' password='ucdcsngl'")
        cur = conn.cursor()

        length = 1
        try:
            query = "SELECT article , newsid,createddate,author from news where ArticleUrl = '" + url + "'"
            # print(query)
            cur.execute(query)
        except:
            print("Unable to select")
        row = cur.fetchone()
        score = None
        createdDate = None
        tempnewsid = None
        article = None
        fullarticle = None
        author = None
        if ( row != None ):

            article=''.join(row[0])
            fullarticle = ''.join(row[0])
            article = smart_truncate(article, 3700)
            article=article.strip()
            article = article.replace("'","")
            article = article.replace("\"","")
            article = article.replace('{', '')
            article = article.replace('}', '')
            article = article.replace('%', '')
            article = article.replace(',', '')
            article = article.replace('\r', '').replace('\n', '')
            article = re.sub(r'[?|$|!]',r'',article)

            # print(""+article+"dfdfd")
            # print(article)
            tempnewsid = row[1]
            createdDate = row[2]
            author = row[3]
            try:
                query = "insert into datasetnewsscore (newsid) values ("+str(tempnewsid)+")"
            
                cur.execute(query)
                conn.commit()
            except:
                print("Already in db")
                print(traceback.format_exc())
            if (article==''):
                print('No content')
            else:
                # print (article)
                response = requests.get("https://api.textgears.com/check.php?text=" +article+ "!&key=BcE9PtP9ptzxjcOH") #BcE9PtP9ptzxjcOH     Db56en2Sg9dDCRqK
                print(response)
                grammar = response.json()
                #return requests.get(grammar).json()
                # print(grammar)
                # print(grammar['score'])
                score = grammar['score']
            # (grammar['result'])

            if (score==None):
                score=0
            try:
                query = "update datasetnewsscore set grammarscore = "+str(score)+" where newsid = " + str(tempnewsid)
                # print(query)
                cur.execute(query)
                conn.commit()
            except:
                print(traceback.format_exc())
        # print("\n\n\n\n Article")
        # print(fullarticle)
        if (fullarticle != None):
            list_number = []
            score_para = 0
            # print(type(fullarticle))
            # fullarticle.replace('{','[')
            # fullarticle.replace('}',']')
            # print(fullarticle)

            # articleList = ast.literal_eval(fullarticle)
            for paragraphs in articleContentList:
                # print(paragraphs)
                length = len(re.findall(r'\w+', paragraphs))
                list_number.append(length)
            # print(list_number)
            max_number = max(list_number)
            query = "update datasetnewsscore set wordcount = "+str(max_number)+" where newsid = " + str(tempnewsid)
            # print(query)
            cur.execute(query)
            conn.commit()
    #         print (max_number)
            
        
        if (createdDate != None):
            # createdDate_str = createdDate.strftime("%Y-%m-%dT%H:%M:%S")
            # fetchedDate_str = time.strftime("%Y-%m-%dT%H:%M:%S")
            # createdDate_str = createdDate.strftime("%Y-%m-%dT%H:%M:%S")
            # fetchedDate_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")    
            
            
            # createdDate_str = datetime.datetime.strptime(createdDate, "%Y-%m-%dT%H:%M:%S")
            # fetchedDate_str = datetime.datetime.strptime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S")  
            # print(datetime.datetime.now())
            # print(createdDate)
            duration = datetime.datetime.now() - createdDate
            # duration = fetchedDate_str - createdDate_str
            query = "update datasetnewsscore set datecheck = "+str(duration.days)+" where newsid = " + str(tempnewsid)
            # print(query)
            cur.execute(query)
            conn.commit()
            
            
        if (author != None):
            # print(url)
            realnewsSet = ["edition.cnn.com","nytimes.com","time.com","bloomberg.com","bbc.com","cnbc.com","abc.net.au","theguardian.com","reuters.com","independent.co.uk"];
            domain = urlparse(url).netloc
            if(domain.startswith('www.')):
                domain = domain.replace("www.","")
            # print(domain)
            if domain in realnewsSet:
                query = "update datasetnewsscore set author = 1 where newsid = " + str(tempnewsid)
                # print(query)
                cur.execute(query)
                conn.commit()
            

            
        # print("Before dataset suburl count"+str(len(SubUrl_list)))
        length = 0
        length = int(len(SubUrl_list))
        if (length != 0):
            query = "update datasetnewsscore set subdomains = "+str(length)+" where newsid = " + str(tempnewsid)
            print(query)
            cur.execute(query)
            conn.commit()
            

            cur.close()
            conn.close()
        
        addScore(tempnewsid)

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
        
        cur.close()
        conn.close()
        return


def addScore(tempnewsid):
    # print("Working"+str(tempnewsid))
    try:
        conn=psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='correctdb' user='postgres' password='ucdcsngl'")
    except:
        print ("I am unable to connect to the database.")
    try:
        if(conn):
            # print("Working"+ str(tempnewsid))
            cur = conn.cursor()

            # cur.execute("SELECT * from datasetnewsscore ORDER BY newsid DESC LIMIT 1") #ORDER BY newsid DESC LIMIT 1
            cur.execute("SELECT * from datasetnewsscore where newsid = "+str(tempnewsid)) #ORDER BY newsid DESC LIMIT 1

            # selectRowScore = cur.data[1][0]
            # selectRowScore = [desc[1] for desc in cur.description]
            # print("Step 1 completed")
            selectRowScore = cur.fetchone()

            newsid = selectRowScore[0]
            grammarscore = selectRowScore[1]
            wordcount = selectRowScore[2]
            subdomains = selectRowScore[4]
            author = selectRowScore[6]
            datecheck = selectRowScore[5]

            if (grammarscore == None):
                grammarscore = 0
            else:
                grammarscore = int(grammarscore/20)
            
                # print('grammerscore 0')

            # if (wordcount == 150):
            if (wordcount > 100):
                wordcount = 5-int((wordcount-100)/5)
                if(wordcount<0):
                    wordcount=0
                # print('wordcount 1')
            elif (wordcount<=100):
                wordcount = 5
            else:
                wordcount=0
                # print('wordcount 0')

            if (subdomains == None or subdomains ==0 ):
                subdomains = 5

                # print(' subdomains 5')
            else:
                subdomains = 0
                # print('subdomains 0')

            if (datecheck == None):
                datecheck = None
                # print('datecheck 1')
            elif (datecheck==0):
                datecheck=10
            else:
                datecheck = int((15-int(math.sqrt(datecheck)))*10/15)
                if(datecheck<0):
                    datecheck = 0
                # print('datecheck 0')

            if (author == 1):
                author = 5
                # print('author 1')
            else:
                author = 0
                # print('author 0')

            query = ("INSERT INTO score (newsid,grammar, wordcount, subdomain, datecheck, author) VALUES (%s,%s, %s, %s, %s, %s);")
            data = (str(tempnewsid ), grammarscore, wordcount, subdomains, datecheck, author)
            # print("Step 2 completed")
            cur.execute(query, data)
            conn.commit()
            cur.close()
            conn.close()
    except:
        print ("Score not completed.")    
        print(traceback.format_exc())


jsonData = {
  "defenddemocracy.press" : {
    "language" : "en",
    "type" : "bias",
    "notes" : "editorial board as stated on about us seem to be legitimate academics, and originally authored content byline are academics, although not able to find a clear link between edu pages and these authors' work on this website. Many 3rd party articles are linked, sources provided. These articles are aggregated from other more clearly biased sites i.e. world socialist web site (wswg.org), rt.com, sputniknews.com."
  },
  "4threvolutionarywar.wordpress.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "aanirfan.blogspot.co.uk" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "abovetopsecret.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "ahtribune.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "allnewspipeline.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "americanlookout.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "americannews.com" : {
    "language" : "en",
    "type" : "fake ",
    "notes" : ""
  },
  "americanpatriotdaily.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "americantoday.news" : {
    "language" : "en",
    "type" : "rumor",
    "notes" : ""
  },
  "americasfreedomfighters.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "amplifyingglass.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "amren.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "amtvmedia.com" : {
    "language" : "en",
    "type" : "rumor",
    "notes" : ""
  },
  "amusmentic.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "ancient-code.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "anonhq.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "assassinationscience.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "attn.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "barenakedislam.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "beehivebugle.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "betootaadvocate.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "bigbluevision.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "bigbluevision.org" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "bignuggetnews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "collective-evolution.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "dcleaks.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "galacticconnection.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "gangstergovernment.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "adobochronicles.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "asia-pacificresearch.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "automotostar.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "awdnews.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : "twitter account deleted?"
  },
  "bients.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "bigbluedimension.com" : {
    "language" : "en",
    "type" : "rumor",
    "notes" : ""
  },
  "blackagendareport.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : "anon submissions"
  },
  "blacklistednews.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "bostonleader.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "buzzfeedusa.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "bvanews.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "celebtricity.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "chaser.com.au" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "christianfightback.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "christiantimesnewspaper.com" : {
    "language" : "en",
    "type" : "rumor",
    "notes" : ""
  },
  "cityworldnews.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "cnnnext.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : "basically an RT video channel"
  },
  "counterinformation.wordpress.com" : {
    "language" : "en",
    "type" : "political",
    "notes" : ""
  },
  "counterpunch.com" : {
    "language" : "en",
    "type" : "political",
    "notes" : "explicit POV - legit authors"
  },
  "counterpunch.org" : {
    "language" : "en",
    "type" : "political",
    "notes" : "explicit POV - legit authors"
  },
  "crystalair.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : "redirects to http://www.cap-news.com/"
  },
  "dailyleak.org" : {
    "language" : "en",
    "type" : "parody",
    "notes" : ""
  },
  "darkmoon.me" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "davidduke.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "davidstockmanscontracorner.com" : {
    "language" : "en",
    "type" : "political",
    "notes" : ""
  },
  "foodbabe.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "lushforlife.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "returnofkings.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "thebeaverton.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "thedailymash.co.uk" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "whydontyoutrythis.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "worldnewsdailyreport.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "wundergroundmusic.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "whatdoesitmean.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "guccifer2.wordpress.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "healthimpactnews.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "healthnutnews.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "henrymakow.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "heresyblog.net" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "holyobserver.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "ihavethetruth.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "in5d.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "indiaarising.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "informationclearinghouse.info" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "informetoday.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "instaworldnews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "intrendtoday.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "intrepidreport.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "investmentresearchdynamics.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "investmentwatchblog.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "itaglive.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "100percentfedup.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "21stcenturywire.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "24newsflash.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "365usanews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "70news.wordpress.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "abcnews.com.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "abcnewsgo.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "abriluno.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "aceflashman.wordpress.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "activistpost.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "addictinginfo.org" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "anonews.co" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "anonnews.co" : {
    "language" : "en",
    "type" : "clickbait ",
    "notes" : ""
  },
  "associatedmediacoverage.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "BB4SP.com" : {
    "language" : "en",
    "type" : "conpiracy",
    "notes" : ""
  },
  "beforeitsnews.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "bigamericannews.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "bigpzone.com" : {
    "language" : "en",
    "type" : "",
    "notes" : "redirects to http://therundownlive.com/ (MZ 12/2)"
  },
  "bipartisanreport.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "bluenationreview.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "borowitzreport.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "breaking911.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "breitbart.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "callthecops.net" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "cap-news.com" : {
    "language" : "en",
    "type" : "fake ",
    "notes" : ""
  },
  "cbsnews.com.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "chicksontheright.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "christwire.org" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "chronicle.su" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "civictribune.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "clickhole.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "coasttocoastam.com" : {
    "language" : "en",
    "type" : "unreliable ",
    "notes" : ""
  },
  "consciouslifenews.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "conservativefiringline.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "conservativeoutfitters.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "conspiracywire.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "countdowntozerotime.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "counterpsyops.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "creambmp.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "dailybuzzlive.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "dailycurrant.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "dailyheadlines.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "dailyheadlines.net" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "dailykos.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "dailynewsbin.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "dailysignal.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "dailywire.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "dcclothesline.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "dcgazette.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "denverguardian.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "derfmagazine.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "disclose.tv" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "disclosuremedia.net" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "downtrend.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "drudgereport.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "drudgereport.com.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "duffleblog.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "duhprogressive.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "EagleRising.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "electionnightgatekeepers.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "embols.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "empireherald.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "empirenews.net" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "endingthefed.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "enduringvision.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "EUTimes.net" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "fprnradio.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "freedomoutpost.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "fusion.net" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "geoengineeringwatch.org" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "globalresearch.ca" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "govtslaves.info" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "gulagbound.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "hangthebankers.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "humansarefree.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "huzlers.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "ifyouonlynews.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "ijr.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "ilovemyfreedom.org" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "infowars.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "intellihub.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "ItMakesSenseBlog.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "jonesreport.com" : {
    "language" : "en",
    "type" : "conspiracy ",
    "notes" : ""
  },
  "landoverbaptist.org" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "lewrockwell.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "liberalamerica.org" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "libertyfederation.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "libertymovementradio.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "libertytalk.fm" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "libertyunyielding.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "libertyvideos.org" : {
    "language" : "en",
    "type" : "conpisracy",
    "notes" : ""
  },
  "lifenews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "lifesitenews.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "lifezette.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "liveactionnews.org" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "madpatriots.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "madworldnews.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "makeamericagreattoday.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "mediamass.net" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "megynkelly.us" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "mrconservative.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "msnbc.website" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "nahadaily.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "nationalreport.net" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "nationindistress.weebly.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "naturalnews.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "nbc.com.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "ncscooper.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "nevo.news" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "newcenturytimes.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "newsbiscuit.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "newsexaminer.net" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "newslo.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : "redirects to http://politicops.com/ (12/2)"
  },
  "Newsmax.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "newsmutiny.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "newsninja2012.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "newswatch28.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "newswatch33.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "newswire-24.com" : {
    "language" : "en",
    "type" : "rumor",
    "notes" : ""
  },
  "newyorker.com/humor" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "nodisinfo.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "northcrane.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "now8news.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "nowtheendbegins.com" : {
    "language" : "en",
    "type" : "conpisracy",
    "notes" : ""
  },
  "occupydemocrats.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "other98.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "pakalertpress.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "patriotnewsdaily" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "politicalears.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "politicalo.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "politicops.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "politicususa.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "prisonplanet.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "prisonplanet.tv" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "prntly.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "realfarmacy.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "realnewsrightnow.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "realtimepolitics.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "redflagnews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "redstate.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "reductress.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "rightalert.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "rightwingnews.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "rilenews.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "satiratribune.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "sonsoflibertyradio.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "sportspickle.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "theblaze.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "thebostontribune.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "thedailysheeple.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "theduran.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "thefreethoughtproject.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "theinformedamerican.net" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "thenewsnerd.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "theonion.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "thepoliticalinsider.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "thereporterz.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "therightstuff.biz" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "thestatelyharold.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "theuspatriot.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "truthfeed.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : ""
  },
  "truthfrequencyradio.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "twitchy.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "ufoholic.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "unconfirmedsources.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "unitedmediapublishing.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "us.blastingnews.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "usapoliticstoday.com " : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "usasupreme.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "usdefensewatch.com" : {
    "language" : "en",
    "type" : "unreliable",
    "notes" : ""
  },
  "usherald.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "usuncut.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "veteranstoday.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "wakingupwisconsin.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "waterfordwhispersnews.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "wikileaks.com" : {
    "language" : "en",
    "type" : "rumors",
    "notes" : ""
  },
  "wikileaks.org" : {
    "language" : "en",
    "type" : "rumors",
    "notes" : ""
  },
  "Willyloman.wordpress.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "winkprogress.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "winningdemocrats.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "witscience.org" : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "wnd.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "worldtruth.tv" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "worldwidehealthy.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "www.rt.com" : {
    "language" : "en",
    "type" : "state",
    "notes" : ""
  },
  "Youngcons.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "yournewswire.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "zerohedge.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "abeldanger.net" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "antiwar.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : "site is biased but very open about bias and source"
  },
  "concisepolitics.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "conservativedailypost.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : "This website is a weird mix of outright fake news and some stuff that looks more credible. "
  },
  "conservativetribune.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "consortiumnews.com" : {
    "language" : "en",
    "type" : "credible",
    "notes" : "The authors on this website are pretty credible and the articles appear well researched"
  },
  "corbettreport.com" : {
    "language" : "en",
    "type" : "conpsiracy",
    "notes" : ""
  },
  "countercurrents.org" : {
    "language" : "en",
    "type" : "political",
    "notes" : "This site is pretty explicit about it's p.o.v. and is coming from a political perspective but doesn't fit under how we are defining 'bias'"
  },
  "dailyoccupation.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "dailypolitics.info" : {
    "language" : "en",
    "type" : " ",
    "notes" : "website now down"
  },
  "dailypoliticsusa.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "dailysquib.co.uk " : {
    "language" : "en",
    "type" : "satire",
    "notes" : ""
  },
  "dailystormer.com" : {
    "language" : "en",
    "type" : "hate",
    "notes" : "pretty well known neo-nazi site"
  },
  "darkpolitricks.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "davidwolfe.com" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "delectabledietofpics.net" : {
    "language" : "en",
    "type" : " ",
    "notes" : "website now down"
  },
  "departed.co" : {
    "language" : "en",
    "type" : "fake",
    "notes" : "redircts to dcposts.com "
  },
  "dineal.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "educate-yourself.org" : {
    "language" : "en",
    "type" : "conspiracy",
    "notes" : ""
  },
  "educateinspirechange.org/health" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "elelephantintheroom.blogspot.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "elitereaders.com" : {
    "language" : "en",
    "type" : "clickbait",
    "notes" : ""
  },
  "elkoshary.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : "About Me notes that it's not fake/satircal news"
  },
  "elmundotoday.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : "About Me notes that it's not fake/satircal news"
  },
  "empiresports.co" : {
    "language" : "en",
    "type" : "satire",
    "notes" : "About Me notes that it's not fake/satircal news"
  },
  "enabon.com" : {
    "language" : "en",
    "type" : "fake",
    "notes" : "No authors, no contact, just copy/pasted from other questionable sites"
  },
  "endoftheamericandream.com" : {
    "language" : "en",
    "type" : "unknown",
    "notes" : "website down"
  },
  "endtime.com" : {
    "language" : "en",
    "type" : "unknown",
    "notes" : "Not sure about this one. zany religious prophecy/not really conspiracy"
  },
  "everythingnewdaily.com" : {
    "language" : "en",
    "type" : "unknown",
    "notes" : "website down"
  },
  "ewao.com" : {
    "language" : "en",
    "type" : "junksci",
    "notes" : ""
  },
  "washingtonsblog.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : "Site notes it sometimes contains parody"
  },
  "westernjournalism.com" : {
    "language" : "en",
    "type" : "bias",
    "notes" : ""
  },
  "dennismichaellynch.com" : {
    "language" : "en",
    "type" : "political",
    "notes" : ""
  },
  "diversitychronicle.wordpress.com" : {
    "language" : "en",
    "type" : "satire",
    "notes" : "self-labled: https://diversitychronicle.wordpress.com/disclaimer/ "
  },
  "english.ruvr.ru" : {
    "language" : "en",
    "type" : "unknown",
    "notes" : "redirects to https://sputniknews.com/ "
  },
  "eutopia.buzz" : {
    "language" : "en",
    "type" : "fake",
    "notes" : ""
  },
  "everydayworldnews.com" : {
    "language" : "en",
    "type" : "unknown",
    "notes" : "website down"
  }
}
