from django.conf.urls import url
from universitytransfer import views
from django.urls import path,re_path

from . import views

urlpatterns = [
    path('helloDynamo', views.helloDynamo, name='helloDynamo'),
	url(r'^$', views.HomePageView.as_view(), name='home'),
	url(r'dynamicgraph', views.DynamicGraphPageView.as_view(), name='dynamicgraph'),    
	url(r'^about/$', views.AboutPageView.as_view(), name='about'),
	re_path(r'^nhti\/([0-9]+\/)?$', views.NHTIPageView.as_view(), name='nhti'),
    url(r'^ajax/getcourse/$', views.getCourses, name='get_course'),
	url(r'^mcc/$', views.MCCPageView.as_view(), name='mcc'),
	url(r'^ncc/$', views.NCCPageView.as_view(), name='ncc'),
]