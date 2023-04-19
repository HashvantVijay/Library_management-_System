from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.publicationlisting, name="publicationlisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<publicationId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<publicationId>\w{0,50})/$', views.delete, name="delete"),
]
