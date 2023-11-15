from django.urls import path

from .views import create_tuotiral_view

urlpatterns = [
    path('create/', create_tuotiral_view, name='create-tutorial'),
]
