# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from engine.models import Article
from . import forms
def home(request):
    return TemplateResponse(request, 'index.html', {'articles': Article.objects.all()[0:10]})

def about(request):
	return TemplateResponse(request, 'about.html', {'articles': Article.objects.all()[0:10]})

def article(request, slug):
	context = {}
	context['article'] = get_object_or_404(Article, slug=slug)
	context['comment_form'] = forms.CommentForm
	context['articles'] = Article.objects.all()[0:10]
	context['meta'] =  get_object_or_404(Article, slug=slug).as_meta(request)
	return TemplateResponse(request, 'article.html', context )