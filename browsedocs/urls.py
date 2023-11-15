from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path, include, re_path


from .views import (support_view, rate_limiter_view, view_404, 
                        handler_403, home_view)

handler404 = view_404

handler403 = handler_403


admin.site.site_header = 'BrowseDocs'           
admin.site.index_title = 'Site Admin'              
admin.site.site_title = 'BrowseDocs admin site'
admin.site.site_url = "https://browsedocs.com" 



urlpatterns = [
    path('admin/', admin.site.urls),    

    
    path("", include('docsapp.urls')),
    # path('docs/', include('docsapp.urls')),
    
    path("", lambda r: redirect("home")),

    path('auth/', include('social_django.urls', namespace='social')),
    
    path('opensource-documentation/', home_view, name='home'),

    path('support/', support_view, name='support-view'),
    path('ratelimit-error/', rate_limiter_view, name='ratelimit-error'),

    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('tutorial/', include('tutorial.urls')),
    


    path("__reload__/", include("django_browser_reload.urls")),

]

if settings.DEBUG:
   urlpatterns +=  []

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   
urlpatterns += [ re_path(r'^.*/$', view_404, name='page_not_found'),]