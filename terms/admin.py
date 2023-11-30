from django.contrib import admin

from . import models

@admin.register(models.Term)
class TermAdmin(admin.ModelAdmin):

    list_display = ['id',  'title', 'datetime']
    search_fields = ['title']   
    