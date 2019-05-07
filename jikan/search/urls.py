from django.conf.urls import url
from django.contrib import admin
from .views import (searchpaper)

urlpatterns = [
     url(r'^$', searchpaper, name='search_paper'),
]
