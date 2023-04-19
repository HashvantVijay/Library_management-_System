from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.booklisting, name="booklisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^update/(?P<bookId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<bookId>\w{0,50})/$', views.delete, name="delete"),
]
