from django.urls import path
from django.shortcuts import redirect

from .views import create_blog_view, save_draft, list_blogs, get_blog

urlpatterns = [

    path('', lambda request: redirect('list-blog', permanent=True), name='list-blog'),
    path('<int:id>/', get_blog, name='get-blog'),
    path('<int:id>/<slug:title>/', get_blog, name='get-blog'),
    path('<str:project_id>/<int:id>/<slug:title>/', get_blog, name='get-blog'),
    
    path('list/', list_blogs, name='list-blogs'),
    path('<str:name>/<str:project_id>/list/', list_blogs, name='list-blogs'),


    path('create/', create_blog_view, name='create-blog'),
    path('save-draft/', save_draft, name='save-draft'),
]
