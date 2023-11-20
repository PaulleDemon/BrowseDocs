from django.urls import path

from .views import (DocsCreateView, ImportRepoView, 
                    check_name_exists, explore_docs, project_list)

urlpatterns = [

    path('docs/create/', DocsCreateView.as_view(), name='docs-create'),
    path('repo/import/', ImportRepoView.as_view(), name='import-repo'),
    path('docs/list/', project_list, name='doc-list'),
    
    path('docs/explore/', explore_docs, name='explore-docs'),
    path('docs/check-name-availability/', check_name_exists, name='name-availabilty'),

    # path('<str:projectid>/', ),
    # path('<str:projectname>/docs/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/<str:chapter>/', ),

]
