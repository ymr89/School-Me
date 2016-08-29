"""
Definition of urls for SchoolMe.
"""

from django.conf.urls import include, url, patterns
from django.contrib import admin
import notifications.urls


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('app.urls')),
    url(r'^profile/', include('app.urls')),
    url(r'^action/', include('app.urls')),
    url(r'^create_profile/', include('app.urls')),
    url(r'^api/', include('app.urls')),
    url(r'^feedbacks/comments/', include('django_comments.urls')),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    

]