from django.urls import path
from django.shortcuts import redirect

from .views import create_tutorial_view, save_draft, list_tutorials, get_tutorial

urlpatterns = [

    path('', lambda request: redirect('list-tutorials', permanent=True), name='list-tutorials'),
    path('<int:id>/', get_tutorial, name='get-tutorial'),
    path('<int:id>/<slug:title>/', get_tutorial, name='get-tutorial'),
    path('<str:project_id>/<int:id>/<slug:title>/', get_tutorial, name='get-tutorial'),
    path('<str:name>/<str:project_id>/list/', list_tutorials, name='list-tutorials'),
    path('<str:project_id>/list/', list_tutorials, name='list-tutorials'),
    path('list/', list_tutorials, name='list-tutorials'),

    path('create/', create_tutorial_view, name='create-tutorial'),
    path('save-draft/', save_draft, name='save-draft'),
]
