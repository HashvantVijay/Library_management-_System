from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.categorylisting, name="categorylisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<categoryId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<categoryId>\w{0,50})/$', views.delete, name="delete"),
]
