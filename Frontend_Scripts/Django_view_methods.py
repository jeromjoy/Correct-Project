def upload (request):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM webapp_news')
        News = cursor.fetchone() # fetchall() may not be the right call here?
        return render(request, 'webapp/upload.html', {'News':News})



def upload (request):
        cursor = connection.cursor()
        URL = 'http://www.bbc.com/news'
        cursor.execute('SELECT count(*)FROM webapp_news WHERE article = %s', [URL])
        News = cursor.fetchone() # fetchall() may not be the right call here?
        return render(request, 'webapp/upload.html', {'News':News})
        
        
        
        
def upload (request):
        cursor = connection.cursor()
        url = 'http://www.bbc.com/news'
        cursor.execute('SELECT last_name FROM webapp_news WHERE articleUrl = %s', [])
        News = cursor.fetchone() # fetchall() may not be the right call here?
        return render(request, 'webapp/upload.html', {'News':News})


