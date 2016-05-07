# -*- coding: utf-8 -*-
from django.contrib import admin
from engine.models import Article , Category, Page, Tag , Comments 

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'time')
admin.site.register(Article, ArticleAdmin)


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Page,PageAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tag,TagAdmin)


class CommentAdmin(admin.ModelAdmin):
 	list_display = ('name' , 'article')
admin.site.register(Comments, CommentAdmin)



class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug_category': ('name',)}
admin.site.register(Category, CategoryAdmin)