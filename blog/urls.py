from django.urls import path

from .views import blog_view

urlpatterns = [
    # path('tutorial/'),
    # path('blog/'),
    path('terms-and-conditions/', blog_view, name='t&c'),
    path('privacy/', blog_view, name='privacy')
]
