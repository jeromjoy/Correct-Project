#
# Create your models here.
#

class News :
    article = None
    title = None
    author = None
    createddate = None
    articleurl = None
    category = None

    def __init__(self,title, article, author,createddate, articleurl):
        self.article = article
        self.title = title
        self.author = author
        self.createddate = createddate
        self.articleurl = articleurl


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

    def __init__(self,title, author,createddate):
        
        self.title = title
        self.author = author
        self.createddate = createddate

class NotFoundNewsApi:
    data = None
    
    def __init__(self):
        self.data = "None"
        

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
        

