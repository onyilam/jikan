from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]