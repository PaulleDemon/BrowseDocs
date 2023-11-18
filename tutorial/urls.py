from django.urls import path

from .views import create_tutorial_view, save_draft

urlpatterns = [
    path('create/', create_tutorial_view, name='create-tutorial'),

    path('save-draft/', save_draft, name='save-draft'),
]
