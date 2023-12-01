from django.urls import path

from .views import (ProjectCreateView, ImportRepoView, 
                    check_name_exists, project_list,
                    get_docs, get_project_about, SearchView,
                    DocCreateView, UpdateDocsView, redirect_shortened_url
                    )

urlpatterns = [

    
    path('search/', SearchView.as_view(), name='search'),
    path('doc/create/', DocCreateView.as_view(), name='doc-create'),
    path('doc/update/', UpdateDocsView.as_view(), name='update-doc'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('repo/import/', ImportRepoView.as_view(), name='import-repo'),
    path('docs/list/', project_list, name='doc-list'),
    
    path('docs/check-name-availability/', check_name_exists, name='name-availabilty'),

    path('<str:name>/about/<str:unique_id>/', get_project_about, name='project-about'),

    path('<str:name>/docs/<str:unique_id>/<str:version>/', redirect_shortened_url, name='get-docs'),
    path('<str:name>/docs/<str:unique_id>/<str:version>/<path:page_url>/', get_docs, name='get-docs'),
    path('<str:name>/docs/<str:unique_id>/', redirect_shortened_url, name='get-docs'),
    path('<str:unique_id>/', redirect_shortened_url, name='get-docs'),
    # path('<str:projectid>/', ),
    # path('<str:projectname>/docs/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/', ),
    # path('<str:projectname>/docs/<str:ln>/v/<str:version>/<str:chapter>/', ),

]
