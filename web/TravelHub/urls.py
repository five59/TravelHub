from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
