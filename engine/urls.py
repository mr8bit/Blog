
# -*- coding: utf-8 -*-
from django.conf.urls import url
from engine.views import article , category , home

__author__ = 'mr. Byte'

urlpatterns = [
	#Url for Home and paginator Home 
    url(r'^$', home, name='home'),
	url(r'^page/(\d+)$', home ),
	
	#Url for Article 
	url(r'^(?P<slug>[-\w]+)$', article, name='article'),

	# Url for Category
	url(r'^category/(?P<slug_category>[-\w]+)/page/(?P<page>[-\d]+)$', category ),
	url(r'^category/(?P<slug_category>[-\w]+)$', category , name='category'),

]