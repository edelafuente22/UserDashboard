from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^process_signin$', views.process_signin),
    url(r'^register$', views.register),
    url(r'^process_registration$', views.process_registration),
    url(r'^dashboard/$', views.dashboard),
    url(r'^dashboard/admin$', views.admin),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^process_message$', views.process_message),
    url(r'^process_comment$', views.process_comment),
    url(r'^logout$', views.logout)
]