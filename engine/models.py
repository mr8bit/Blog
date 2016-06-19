# -*- coding: utf-8 -*-
from django.db import models
from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sitemaps import Sitemap
 

class LikeAriticle(models.Model):
	count_likes = models.IntegerField(default=0)
	ip = models.CharField(max_length=100)
	article = models.ForeignKey('Article')

	class Meta:
		ordering =['-article']
		db_table = 'likeandarticle'


class StaticSitemap(Sitemap):
    def items(self):
        return Page.objects.all()

class BlogSitemap(Sitemap):	
	def items(self):
		return Article.objects.all()

# Модель статьи 
class Article(ModelMeta,models.Model):
	time = models.DateTimeField(verbose_name= u'Дата побликации')# Время добавляется автоматически
	title = models.CharField(max_length=100) # Название статьи с мак. кол. букв 100
	slug = models.SlugField()
	meta_keywords = models.TextField(verbose_name= u'SEO keywords', blank=True, default='')
	meta_description = models.TextField(verbose_name= u'SEO description', blank=True, default='')
	summary = RichTextUploadingField(blank=True, default='', verbose_name='Краткое описание')
	content = RichTextUploadingField(blank=True, default='', verbose_name='Статья')
	category = models.ManyToManyField('Category', default='')
	tags = models.ManyToManyField('Tag', default='')	  
	likes = models.IntegerField(default=0)

	def __str__(self):
		return self.title
	class Meta:
		ordering =['-time']
	_metadata = {
		'title': 'title',
		'use_title_tag': 'True',
		'description': 'get_description',
		'keywords': 'get_keywords',
		'object_type': 'Article',
        'og_type': 'Article'
	}
	def get_absolute_url(self):
		return "/article/"+self.slug+"/"
 
    
 

	def get_keywords(self):
		return self.meta_keywords.strip().split(',')

	def get_description(self):
		description = self.meta_description
		if  not description:
			description = self.summary
		return description.strip()


class Comments(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200,verbose_name=u'Имя')
	email = models.EmailField(max_length=200)
	comment = RichTextUploadingField(verbose_name=u'Комментарий')
	article = models.ForeignKey('Article')
	ip = models.CharField(max_length=100, default=' ')
	anser_on = models.ForeignKey('self',blank=True, null=True)

	def __str__(self):
		return self.email

	class Meta:
		ordering =['-time']
		db_table = 'comments'
STATUS_CHOICES = (
    ('p', 'Страница'),
    ('c', 'Категория'),
)
class Category(ModelMeta, models.Model):
	name = models.CharField(max_length=255, verbose_name = 'Название')
	slug_category = models.SlugField()
	sort_in_menu = models.CharField(max_length=255, verbose_name = 'Сортировка меню',default='')
	type_menu = models.CharField(max_length=1,choices=STATUS_CHOICES, default='')
	meta_keywords = models.TextField(verbose_name= u'SEO keywords', blank=True, default='')
	meta_description = models.TextField(verbose_name= u'SEO description', blank=True, default='')
	page = models.ForeignKey('Page' , blank=True , null=True)
	_metadata = {
		'title': 'name',
		'use_title_tag': 'True',
		'description': 'get_description',
		'keywords': 'get_keywords', 
	}
	def __str__(self):
		return self.name
	def get_keywords(self):
		return self.meta_keywords.strip().split(',')
	def get_description(self):
		description = self.meta_description
		return description.strip()
	class Meta:
		db_table='categorys'

class Page(ModelMeta,models.Model):
	title = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField()
	meta_keywords = models.TextField(verbose_name= u'SEO keywords', blank=True, default='')
	meta_description = models.TextField(verbose_name= u'SEO description', blank=True, default='')
	content = RichTextUploadingField(blank=True, null = True, default='',verbose_name=u'Содержание страницы')

 
	_metadata = {
		'title': 'title',
		'use_title_tag': 'True',
		'description': 'get_description',
		'keywords': 'get_keywords',
 	}
	def __str__(self):
		return self.title
	def get_description(self):
		description = self.meta_description
	def get_keywords(self):
		return self.meta_keywords.strip().split(',')
	def get_absolute_url(self):
		return "/"+self.slug
 
class Tag(ModelMeta,models.Model):
	name = models.CharField(max_length=255)
	slug = models.CharField(max_length=255)
	meta_keywords = models.TextField(verbose_name= u'SEO keywords', blank=True, default='')
	meta_description = models.TextField(verbose_name= u'SEO description', blank=True, default='')
	

	_metadata = {
	'title': 'name',
	'use_title_tag' : 'True',
	'description' : 'get_description',
	'keywords': 'get_keywords',
 	}
	def __str__(self):
		return self.name
	def get_description(self):
		description = self.meta_description
	def get_keywords(self):
		return self.meta_keywords.strip().split(',')
 
 