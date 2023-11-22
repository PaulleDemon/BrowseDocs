from django.contrib import admin

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
class ProjectAdmin(admin.ModelAdmin):

    list_display = ['id', 'project', 'lang', 'version',]

    list_filter = ['datetime']
