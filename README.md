# Correct News Indicator
After the recent American elections, the issue about fake news (or unreliable, conspiracy, satire, hate, bias, junk, political, clickbait) has surfaced. We have all seen the how spread of fake and conspiratorial news impacted elections in one world’s most powerful countries. There have been many more such instances where people have considered fake or modified news as reality and have responded in a negative way. These have caused impact on politics, health and so on. To prevent people from believing such fake, unreliable, bias, junk, etc. news spread through social media, we decided to build a system which will help reduce the spread and bring people to reality about the news worldwide.


You can use our system live at  http://137.43.49.13:8000/home/ (When using from ucd campus please use eduroam wifi access)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites

Python 3.6  
Postgressql  

The above system was built for linux machine.


### Setting up virtual environment

https://docs.python.org/3/tutorial/venv.html

The module used to create and manage virtual environments is called venv.
To create a virtual environment, decide upon a directory where you want to place it, and run the venv module as a script with the directory path:

python3 -m venv tutorial-env

This will create the tutorial-env directory if it doesn’t exist, and also create directories inside it containing a copy of the Python interpreter, the standard library, and various supporting files.

Once you’ve created a virtual environment, you may activate it.

On the machine, run:

```
source tutorial-env/bin/activate
```

You can install, upgrade, and remove packages using a program called pip.

pip install django

Similarly install the libraries below  
beautifulsoup4 (4.6.0)  
chardet (3.0.4)  
dateparser (0.6.0)  
django-celery (3.2.1)  
pip (9.0.1) 
pkg-resources (0.0.0) 
psycopg2 (2.7.1)  
python-dateutil (2.6.0)  
regex (2017.7.28)  
requests (2.18.1)  




After installing all the files move the project TC_APP to your folder.  
Navigate to TC_App/Team_Correct_App/ and run the below code 


```
python manage.py runserver 0:8000
```


## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Postgres](https://www.postgresql.org/) - PostgreSQL is a powerful, open source object-relational database system



## Authors

* **Michael Brennan** - [Michael](https://github.com/MichaelBrennan83)
* **Kunal Chavan** - [Kunal](https://github.com/kunalc28)
* **Ketaki Abhay Ghatage** - [Ketaki](https://github.com/Ketakighatage)
* **Xiaosheng Liang** - [Xiaosheng](https://github.com/XiaoshengLiang)
* **Jerom Joy Vattakeril** - [Jerom](https://github.com/jeromjoy)



## License

This project is licensed under the MIT License 

## Acknowledgments

* Opensource project (https://github.com/BigMcLargeHuge/opensources) (http://www.opensources.co/) - Professionally curated lists of online sources, available free for public use.
* B.S. Detector (http://bsdetector.tech/) -A browser extension for both Chrome and Mozilla-based browsers 
* NewsApi - (https://newsapi.org/) - News API is a simple and easy-to-use API that returns JSON metadata for the headlines currently published on a range of news sources and blogs 

* NewsApi - (https://newsapi.org/) - News API is a simple and easy-to-use API that returns JSON metadata for the headlines currently published on a range of news sources and blogs 
* Snopes - (http://www.snopes.com/) - The definitive Internet reference source for urban legends, folklore, myths, rumors, and misinformation. 
