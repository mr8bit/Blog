# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from engine.models import Article , Category
from django.core.paginator import Paginator
from . import forms
def home(request , page =1):
	context = {}
	context['articles'] = Article.objects.all()
	context['category'] = Category.objects.all().order_by('sort_in_menu')
	paginator = Paginator(context['articles'],10)
	try:
		context['articles'] = paginator.page(page)
	except PageNotAnInteger:
		context['articles'] = paginator.page(1)
	except EmptyPage:
		context['articles'] = paginator.page(paginator.num_pages)
	return TemplateResponse(request, 'index.html', context )


def article(request, slug):
	context = {}
	context['article'] = get_object_or_404(Article, slug=slug)
	context['comment_form'] = forms.CommentForm
	context['meta'] =  get_object_or_404(Article, slug=slug).as_meta(request)
	return TemplateResponse(request, 'article.html', context )



def category(request,slug_category,page=1):
	context={}
	context['categor'] = Category.objects.get(slug_category = slug_category)
	context['meta'] =  get_object_or_404( Category, slug_category=slug_category).as_meta(request)
	context['articles'] = Article.objects.filter(category=context['categor'].id)
	context['category'] = Category.objects.all().order_by('sort_in_menu')
	paginator = Paginator(context['articles'],10)
	try:
		context['articles'] = paginator.page(page)
	except PageNotAnInteger:
		context['articles'] = paginator.page(1)
	except EmptyPage:
		context['articles'] = paginator.page(paginator.num_pages)
	return TemplateResponse(request , 'category.html', context)