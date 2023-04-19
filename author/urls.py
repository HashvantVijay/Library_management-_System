from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.authorlisting, name="authorlisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<authorId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<authorId>\w{0,50})/$', views.delete, name="delete"),
]
