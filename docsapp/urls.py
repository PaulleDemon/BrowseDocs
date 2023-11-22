from django.urls import path

from .views import (DocsCreateView, ImportRepoView, 
                    check_name_exists, project_list,
                    get_docs, get_project_about
                    )

urlpatterns = [

    
    path('docs/create/', DocsCreateView.as_view(), name='docs-create'),
    path('repo/import/', ImportRepoView.as_view(), name='import-repo'),
    path('docs/list/', project_list, name='doc-list'),
    
    path('docs/check-name-availability/', check_name_exists, name='name-availabilty'),

    path('<str:name>/about/<str:unique_id>/', get_project_about, name='project-about'),
    path('<str:name>/docs/<str:unique_id>/', get_docs, name='get-docs'),
    path('<str:unique_id>/', get_docs, name='get-docs'),
    # path('<str:projectid>/', ),
    # path('<str:projectname>/docs/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/<str:chapter>/', ),

]
