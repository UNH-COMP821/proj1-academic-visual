from django.conf.urls import url
from universitytransfer import views
from django.urls import path

from . import views

urlpatterns = [
    path('helloDynamo', views.helloDynamo, name='helloDynamo'),
	url(r'^$', views.HomePageView.as_view(), name='home'),
	url(r'dynamicgraph', views.DynamicGraphPageView.as_view(), name='dynamicgraph'),    
	url(r'^about/$', views.AboutPageView.as_view(), name='about'),
	url(r'^nhti/$', views.NHTIPageView.as_view(), name='nhti'),
	url(r'^mcc/$', views.MCCPageView.as_view(), name='mcc'),
	url(r'^ncc/$', views.NCCPageView.as_view(), name='ncc'),
]