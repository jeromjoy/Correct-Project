import traceback
import psycopg2
import os
import urllib.request
import json

class Domain_url(object):
    name=""
    type1=""
    type2=""
    type3=""
    
    def _init_(self, name,type1,type2,type3):        
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3


connectionString = "dbname='correctdb' user='postgres' host='localhost' password='ucdcsngl'"

def addToDBDomainFilter(url,type):
    
    try:
        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()
        
        
        # publishedAt = time.mktime(datetime.datetime.strptime(PublishedAt, "%Y-%m-%d").timetuple())

        cur.execute("INSERT INTO domainfilterlist (url, domaintype) VALUES (%s, %s)", (url, type))
        conn.commit();
        cur.close()
        
    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
    return


def get_raw_data():
    link = "https://raw.githubusercontent.com/BigMcLargeHuge/opensources/master/sources/sources.json"

    get_and_write_data(link)

def get_and_write_data(link):
    response = urllib.request.urlopen(link)
    html = response.read().decode()
    data_dic = json.loads(html)

    keys = list(data_dic.keys())
    values = list(data_dic.values())
    for i in range(len(data_dic)):
        tempName = keys[i]
        if(values[i]['type']):
            tempType1 = values[i]['type']
            addToDBDomainFilter(tempName, tempType1)
            if(values[i]['2nd type']):
                tempType2 = values[i]['2nd type']
                addToDBDomainFilter(tempName, tempType2)
                if(values[i]['3rd type']):
                    tempType3 = values[i]['3rd type']
                    addToDBDomainFilter(tempName, tempType3)
            
        
#         domain = Domain_url(tempName,tempType1,tempType2,tempType3)
        
get_raw_data()