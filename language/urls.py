from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.languagelisting, name="languagelisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<languageId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<languageId>\w{0,50})/$', views.delete, name="delete"),
]
