from django.conf.urls import url
from universitytransfer import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^data/$', views.DataPageView.as_view(), name='data'),  # Add this URL pattern
]
