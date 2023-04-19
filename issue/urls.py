from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.issuelisting, name="issuelisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<issueId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<issueId>\w{0,50})/$', views.delete, name="delete"),
]
