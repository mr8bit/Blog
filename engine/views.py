# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404 , redirect
from django.template.response import TemplateResponse
from engine.models import Article , Category , Page ,Comments ,LikeAriticle , Tag
from django.core.paginator import Paginator
from . import forms
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage , send_mail

def home(request , page =1):
	context = {}
	context['tags'] =  Tag.objects.all()
	context['meta'] =  get_object_or_404( Page, slug="main_page").as_meta(request)
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
	context['tags'] =  Tag.objects.all()
	context['article'] = get_object_or_404(Article, slug=slug)
	context['comment_form'] = forms.CommentForm
	context['meta'] =  get_object_or_404(Article, slug=slug).as_meta(request)
	context['category'] = Category.objects.all().order_by('sort_in_menu')
	context['likecount']=len(LikeAriticle.objects.filter(article=context['article']))
	context['comment'] = Comments.objects.filter(article=context['article'].id).order_by('time')
	if request.POST:
		form = forms.CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.time = datetime.now()
			comment.article = Article.objects.get(slug=slug)
			comment.ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
			if(comment.anser_on_id):
				sendMail(comment , comment.anser_on_id , request)
			adminMail(comment ,request)
			form.save()
			return redirect('/article/%s' % slug)
		else: 
			context['comment_form'] = form
	else:
		context['comment_form'] = forms.CommentForm
	return TemplateResponse(request, 'article.html',context )


def category(request,slug_category,page=1):
	context={}
	context['tags'] =  Tag.objects.all()
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


def page(request , slug):
	context={}
	context['tags'] =  Tag.objects.all()
	context['page'] = get_object_or_404(Page , slug=slug)
	context['meta'] =  get_object_or_404(Page, slug=slug).as_meta(request)
	context['category'] = Category.objects.all().order_by('sort_in_menu')

	return TemplateResponse(request,'page.html',context)


def i_like_it(request, slug):
	article = Article.objects.get(slug=slug)
	like = LikeAriticle.objects.filter(article = article.id) 
	ipis = {}
	for ips in like:
		ipis = ips.ip
	likes=0
	ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
	if ip not in ipis:
			likes = article.likes + 1
			article.likes = likes
			nn = LikeAriticle(ip=ip, article=article)
			nn.save()
			article.save()
	return redirect('/article/%s' % slug )

def  tag(request , slug , page=1):
	context={}
	context['tags'] =  Tag.objects.all()
	context['tag'] = get_object_or_404(Tag,slug = slug)
	context['articles'] = Article.objects.filter(tags=context['tag'])
	context['category'] = Category.objects.all().order_by('sort_in_menu')
	paginator = Paginator(context['articles'],10)
	try:
		context['articles'] = paginator.page(page)
	except PageNotAnInteger:
		context['articles'] = paginator.page(1)
	except EmptyPage:
		context['articles'] = paginator.page(paginator.num_pages)
	return TemplateResponse(request , 'tag.html', context)


def sendMail(comment, to_answer, reques): 
	comment_to_answer = get_object_or_404(Comments, id=to_answer)
	msg = EmailMessage('Mr.Byte blog: Вам ответил '+comment.name, "<div><h1> Вас приведствует сайт Mr.Byte blog </h1></br><h5>Недавно вам ответили на ваш впорос, " +str(comment.name)+ "</h5></br>" +str(comment.comment)+ '<h4>Для ответа прейдите по ссылке <a href="'+str(reques.get_full_path())+'">Ответить</a></h4></div>' , settings.EMAIL_HOST_USER, [comment_to_answer.email])
	msg.content_subtype = "html"
	msg.send()

def adminMail(comment,reques):
	answer = "<h1> Вас приведствует сайт Mr.Byte blog </h1></br><h3>Время "+str(comment.time)+"</h3><h4>Недавно вам оставил комментарий, " + str(comment.name)  + "</h5></br>"+str(comment.comment)+'<div>Для ответа прейдите по ссылке <a href="%s">Ответить</a></div>' % reques.get_full_path()
	msg = EmailMessage('У вас новый комментарий от пользователя '+comment.name,answer,settings.EMAIL_HOST_USER,['simplex.bro@gmail.com'] )
	msg.content_subtype = "html"
	msg.send()