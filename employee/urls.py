from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login"),
    url(r'^employee-record$', views.employeelisting, name="employeelisting"),
    url(r'^employee-add$', views.add, name="add"),
    url(r'^update/(?P<employeeId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
]	
