from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda _: redirect("t&c")),
    path('terms-and-conditions/', views.t_and_c_view, name='t&c'),
    path('privacy/', views.privacy_view, name='privacy')

]
