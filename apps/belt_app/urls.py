from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^addquote/(?P<id>\d+)$', views.addquote),
    url(r'^fav/(?P<id>\d+)/(?P<uid>\d+)$', views.fav),
    url(r'^view/(?P<id>\d+)$', views.view),
    url(r'^remove/(?P<id>\d+)/(?P<uid>\d+)$', views.remove),
    url(r'^logout$', views.logout),
    ]
