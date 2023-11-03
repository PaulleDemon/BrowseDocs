from django.urls import path

from .views import DocsCreateView, ImportRepoView

urlpatterns = [

    path('docs/create/', DocsCreateView.as_view(), name='docs-create'),
    path('repo/import/', ImportRepoView.as_view(), name='import-repo'),
    
    # path('<str:projectid>/', ),
    # path('<str:projectname>/docs/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/<str:chapter>/', ),

]
