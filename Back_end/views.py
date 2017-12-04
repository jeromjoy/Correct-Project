from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db import connection
import psycopg2
from urllib.parse import urlparse
#from django.db import models
from webapp.models import News




from django.shortcuts import render

from webapp.forms import CostForm

from webapp.models import Cost
from django.template import Context, loader

from webapp.models import URL

import re







def index(request):
    if request.method == 'POST':

        # form = CostForm(request.POST)

        # if form.is_valid():

            url = request.POST.get('url','')

            cost_obj = URL(url=url)

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
            else:
                print('error')
            cost_obj.save()

            template = loader.get_template("webapp/home.html")
            return HttpResponse(template.render())

    else:

        form = CostForm()

    return render(request, 'webapp/home.html')


def upload(request):
    return render(request, 'webapp/upload.html')



# getData(url):
# return value
#         return render(request, 'webapp/upload.html', {'p':p})


def search(request):
    t = request.GET.get('search', 'Not found')
    News= getData(t)
    if (News == None):
        return render(request, 'webapp/None.html')
    return render(request, 'webapp/temp.html', {'News':News})

    #return HttpResponse(text+text2, {'News':News})




def getData (value):
        #conn=psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='Correct server' user='postgres' password='ucdcsngl⁠⁠⁠⁠'")
        cursor = connection.cursor()
        parsed_uri = urlparse(value)
        domain = parsed_uri.netloc

        temp=value
        temp=temp.replace("http://","")
        temp=temp.replace("https://","")
        temp=temp.replace("www","")
        temp=temp.replace("/","")
        temp=temp.replace(".html","")
        temp=temp.replace(".php","")
        temp=temp.replace(".","")
        temp=temp.replace("_","")
        temp=temp.replace("-","")
        temp=temp.strip(' \t\n\r')
        #cursor.execute('SELECT articleurl,s.score FROM news,domainfilterlist d,domaintypescore s where articleurl=%s', [domain])
        query = "SELECT  n.title, n.article, n.author, n.createddate, n.fetcheddate, n.articleurl, s.score, d.domaintype FROM news n left outer join domainfilterlist d on d.url ='"+ domain + "' left outer join domaintypescore s on s.type = d.domaintype where n.urlsearch= '"+ temp +"'";
        #cursor.execute('SELECT articleurl,s.score FROM news,domainfilterlist d,domaintypescore s where articleurl=%s', [domain])
        print(query)
        cursor.execute(query)
        # News="hello"
        row = cursor.fetchone() # fetchall() may not be the right call here?
        # for row in rows:
        if (row == None ):
            return None
        if (row[6] == None ):
            data = News(row[0],"",row[2],row[3],row[4],row[5],None,row[7])
        elif (row[6] < 10 ):
            data = News(row[0],"",row[2],row[3],row[4],row[5],row[6],row[7])
        else:
            data = News(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        return data


# query = "SELECT  articleurl,s.score
# 	FROM news,domainfilterlist d,domaintypescore s where articleurl= '"+ value +"'
#      and d.url ='"+ domain + "'
#      and s.type = d.domaintype order by s.score asc";

# def upload (request):
#         cursor = connection.cursor()
#         lname = 'http://americannews.com/michelle-obama-runs-mouth-melania-trump-gets-brutally-slapped/'
#         cursor.execute('SELECT title FROM news WHERE articleurl = %s', [lname])
#         p = cursor.fetchone() # fetchall() may not be the right call here?
#         return render(request, 'webapp/home.html', {'p':p})
