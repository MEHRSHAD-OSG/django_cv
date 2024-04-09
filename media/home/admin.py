from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user' , 'created' , 'slug']
    search_fields = ['slug','body']
    list_filter = ['updated']
    prepopulated_fields = {'slug':['body']}
    raw_id_fields = ['user']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post' ,'body', 'is_reply']
    search_fields = ['user','post']
    raw_id_fields = ['user','post','reply']


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id','user','post']
    search_fields = ['user','post']
    raw_id_fields = ['user','post']