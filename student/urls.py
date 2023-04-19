from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.studentlisting, name="studentlisting"),
    url(r'^update/(?P<studentId>\w{0,50})/$', views.update, name="update"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete/(?P<studentId>\w{0,50})/$', views.delete, name="delete"),
]
