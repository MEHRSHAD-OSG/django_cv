from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.


@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['id','from_user','to_user']


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False

class ExtenderUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User,ExtenderUserAdmin)