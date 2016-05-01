# -*- coding: utf-8 -*-
from django.db import models
from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField

class Article(ModelMeta,models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    meta_keywords = models.TextField(verbose_name= u'SEO keywords', blank=True, default='')
    meta_description = models.TextField(verbose_name= u'SEO description', blank=True, default='')
    summary = RichTextUploadingField(blank=True, default='', verbose_name='Краткое описание')
    content = RichTextUploadingField(blank=True, default='', verbose_name='Статья')
  
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