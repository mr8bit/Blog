
# -*- coding: utf-8 -*-
from django.conf.urls import url
from engine.models import BlogSitemap, StaticSitemap
from engine.views import article , category , home , i_like_it , tag , page

__author__ = 'mr. Byte'

sitemaps = {
	'posts': BlogSitemap,
	'static': StaticSitemap,
}

urlpatterns = [
	#Url for Page
	url(r'^(?P<slug>[-\w]+)$' ,page , name='page' ),
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

	#Url for Tag 
	url(r'^tag/(?P<slug>[-\w]+)$', tag, name='tag'),
	url(r'^tag/(?P<slug>[-\w]+)/page/(?P<page>[-\d]+)$', tag),

	#Url for Home and paginator Home 
    url(r'^$', home, name='home'),
	url(r'^page/(\d+)$', home ),
	
	#Url for Article 
	url(r'^article/(?P<slug>[-\w]+)$', article, name='article'),
	url(r'^ilikeit/(?P<slug>[-\w]+)/$', i_like_it , name='i_like_it'),

	# Url for Category
	url(r'^category/(?P<slug_category>[-\w]+)/page/(?P<page>[-\d]+)$', category ),
	url(r'^category/(?P<slug_category>[-\w]+)$', category , name='category'),

]