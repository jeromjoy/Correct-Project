import requests
# from pprint import pprint
import psycopg2
import re




def newcall():
    try:
        conn=psycopg2.connect("host='csi6220-1-vm2.ucd.ie' dbname='correctdb' user='postgres' password='ucdcsngl'")
        cur = conn.cursor()

        length = 1
        while(length>0):
            query = "SELECT newsid from datasetnewsscore where grammarscore is NULL  limit 1"
            print(query)
            cur.execute(query)
            rows = cur.fetchall()
            # print (rows)
            length = len(rows)
            if(length==0):
                break;
            tempnewsid=''

            for row in rows:
                tempnewsid=str(row[0])
                query = """SELECT article from news  where newsid = """+tempnewsid
                print (tempnewsid)

                # length = len(articlerows)
            cur.execute(query)

            rows = cur.fetchall()
            score = None

            for row in rows:
                article=''.join(row[0])
                article=article.strip()
                article = article.replace("'","")
                article = article.replace("\"","")
                # article = article.replace('{', '')
                # article = article.replace('}', '')
                # article = article.replace('%', '')
                # article = article.replace(',', '')
                # article = article.replace('\r', '').replace('\n', '')
                # article = re.sub(r'[?|$|!]',r'',article)

                # print(""+article+"dfdfd")
                # print(article)
                if (article==''):
                    print('No content')
                else:
                    print (article)
                    response = requests.get("https://api.textgears.com/check.php?text=" +article+ "!&key=Db56en2Sg9dDCRqK")
                    print(response)
                    grammar = response.json()
                    return requests.get(grammar).json()

                    print(grammar)
                    score = grammar['score']
                # (grammar['result'])
            score=0
            if (score!=None):
                query = "update datasetnewsscore set grammarscore = "+str(score)+" where newsid = " + str(tempnewsid)
                print(query)
                cur.execute(query)
                conn.commit()


        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("I am unable to connect to the database")
        print(e)
        print(e.pgcode)
        print(e.pgerror)
        print(traceback.format_exc())
        conn.commit()
        cur.close()
        conn.close()
        return


newcall()
