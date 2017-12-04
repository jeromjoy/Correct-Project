

import urllib.request
import requests
import json

import requests
from bs4 import BeautifulSoup
import time
import traceback
import psycopg2
import datetime

connectionString = "dbname='correctdb' user='postgres' host='localhost' password='ucdcsngl'"
conn = psycopg2.connect(connectionString)

def uploadDBNewsApi(newsApi):

    try:

        cur = conn.cursor()


        # publishedAt = time.mktime(datetime.datetime.strptime(PublishedAt, "%Y-%m-%d").timetuple())

        cur.execute("INSERT INTO NewsFetchedApi (Url, Author, Title, Description, ImageUrl, PublishedAt) VALUES (%s, %s, %s, %s, %s, %s)", (Url, Author, Title, Description, ImageUrl, PublishedAt))
        conn.commit();
        cur.close()

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return



def uploadDBNews(news):

    try:

        cur = conn.cursor()

        # createdDate = time.mktime(datetime.datetime.strptime(CreatedDate, "%d/%m/%Y").timetuple())
        # fetchedDate = time.mktime(datetime.datetime.strptime(FetchedDate, "%d/%m/%Y").timetuple())
        # lastUsed = time.mktime(datetime.datetime.strptime(LastUsed, "%d/%m/%Y").timetuple())


        cur.execute("INSERT INTO News (Article, Title, Author, OriginalContent, CreatedDate, FetchedDate,ArticleUrl,LastUsed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (news.Article, news.Title, news.Author, news.OriginalContent, news.CreatedDate, news.FetchedDate, news.ArticleUrl, news.LastUsed))
        conn.commit();
        cur.close()

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return

