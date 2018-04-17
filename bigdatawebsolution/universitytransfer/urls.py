from django.conf.urls import url
from universitytransfer import views
from django.urls import path
from . import views

urlpatterns = [
    path(r'detail/<int:question_id>', views.detail, name='detail'),
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^data/$', views.DataPageView.as_view(), name='data'),  # Add this URL pattern
]
