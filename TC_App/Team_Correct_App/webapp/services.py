
from urllib.parse import urlparse
from webapp.models import News,Domain,WordCount,DateCheck,Author,Grammar,SubUrl,TotalScore,NewsArticle
import re
from webapp.errorTrace import handleErrorTracePsyco,handleErrorTrace
import traceback
import math
from django.shortcuts import render
import datetime
from webapp.jsonResource import realnewsSet
import psycopg2
import requests

# 
# Database connection using psycopg
# 
def connection():
    return psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='correctdb' user='postgres' password='ucdcsngl'")

# 
# Upload Scraped news data to News table
# 
def uploadDBNews(news):

    try:        
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO News (Article, Title, Author, OriginalContent, CreatedDate, FetchedDate,ArticleUrl,LastUsed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (news.Article, news.Title, news.Author, news.OriginalContent, news.CreatedDate, news.FetchedDate, news.ArticleUrl, news.LastUsed))
        conn.commit();
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        handleErrorTracePsyco(e)
    return

# 
# Convert content to text format for evaluation for text in list format
# 
def convertToContent(contentArticle):
    
    contentArticle = contentArticle.replace("'","")
    contentArticle = contentArticle.replace("\"","")
    contentArticle = contentArticle.replace('{', '')
    contentArticle = contentArticle.replace('}', '')
    contentArticle = contentArticle.replace('%', '')
    contentArticle = contentArticle.replace(',', '')
    contentArticle = contentArticle.replace('\r', '').replace('\n', '')
    contentArticle = re.sub(r'[?|$|!]',r'',contentArticle)
    return contentArticle

# 
# Get data from news table and return score for news url request
# 
def getData (value):
    
        conn = connection()
        cursor = conn.cursor()
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
        contentArticle = newsRow[1].strip()
        content = convertToContent(contentArticle)
        
        
        data =  News(newsRow[0],smart_truncate(content),newsRow[2],newsRow[3],newsRow[4])
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
# 
# Calculate the score for the article
# 
def addScore(tempnewsid):
    # print("Working"+str(tempnewsid))
    try:
        conn=connection()
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


# 
# https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
# 
def smart_truncate(content, length=250, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


# 
# Handle error to return error msg on the view
# 
def errorHandle(request,errorText="Site is facing some issues."):
    form = errorText
    print('error')
    return render(request, 'webapp/home.html',{'form': form})

# 
# Collect dataset values to calculate feature score based on the feature properties
# 
def collectDataSet(url,articleContentList,subUrllength):
    
    conn=connection()
    cur = conn.cursor()
    tempnewsid = None
    try:

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
        
        article = None
        fullarticle = None
        author = None
        if ( row != None ):

            article=''.join(row[0])
            fullarticle = ''.join(row[0])
            article = smart_truncate(article, 3700)
            article=article.strip()
            article = convertToContent(article)
            
            tempnewsid = row[1]
            createdDate = row[2]
            author = row[3]
            try:
                query = "insert into datasetnewsscore (newsid) values ("+str(tempnewsid)+")"
            
                cur.execute(query)
                conn.commit()
            except:
                print("Already in db")
                handleErrorTrace()
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
                handleErrorTrace()
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
            
            duration = datetime.datetime.now() - createdDate
            query = "update datasetnewsscore set datecheck = "+str(duration.days)+" where newsid = " + str(tempnewsid)
            # print(query)
            cur.execute(query)
            conn.commit()
            
            
        if (author != None):
            # print(url)
            
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
        
        if (subUrllength != 0):
            query = "update datasetnewsscore set subdomains = "+str(subUrllength)+" where newsid = " + str(tempnewsid)
            print(query)
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
        
    except psycopg2.Error as e:
        handleErrorTracePsyco(e)
        
        cur.close()
        conn.close()
    return tempnewsid