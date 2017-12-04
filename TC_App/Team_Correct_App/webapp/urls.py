from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$', views.index, name = 'index'),
    # url(r'^upload-file/$', views.upload, name='page'),
    url(r'^search/', views.search, name='search'),
    url(r'^searchapi/', views.searchApi, name='searchApi')


]
