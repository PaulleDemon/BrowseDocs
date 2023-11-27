from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.html import format_html

from lxml.html.clean import clean_html

from .models import (Project, Social, Sponsor, AdditionalLink,
                        Documentation, DocPage)


class InlineSocial(admin.StackedInline):

    model = Social
    extra = 0

class InlineSponsor(admin.StackedInline):

    model = Sponsor
    extra = 0


class InlineLink(admin.StackedInline):

    model = AdditionalLink
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'unique_id', 'unique_name', 'user', 'datetime']
    search_fields = ['name', 'unique_name', 'unique_id']

    list_filter = ['datetime']

    inlines = [InlineSocial, InlineSponsor, InlineLink]


@admin.register(Documentation)
class DocsAdmin(admin.ModelAdmin):

    list_display = ['id', 'project', 'lang', 'version',]

    list_filter = ['datetime']


@admin.register(DocPage)
class DocPageAdmin(admin.ModelAdmin):

    list_display = ['id', 'page_url', 'documentation', 'body',]

    list_filter = ['datetime']
    readonly_fields = ['body_html', 'datetime', 'id']

    fieldsets = (
        (None, {
            'fields': ('id', 'page_url', 'documentation', 'datetime')
        }),
        ('Body', {
            'fields': ('body', 'body_html'),
            'classes': ('wide',),
        }),
    )


    def body_html(self, obj):
        return mark_safe(clean_html(obj.body.html))
        