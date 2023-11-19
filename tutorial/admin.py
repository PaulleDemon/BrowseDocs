from django.contrib import admin

from .models import Tutorial

# Register your models here.
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    
    search_fields = ['title']
    list_display = ['id', 'title', 'datetime', 'draft', 'published']
    list_filter = ['datetime', 'published', 'draft']

    def titl(self, obj):
        return obj.title[:10]