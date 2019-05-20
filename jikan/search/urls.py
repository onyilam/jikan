from django.conf.urls import url
from .views import searchpaper, get_recommendation, HomePageView, postpreference
from django.urls import path

urlpatterns = [
     url(r'recommendation/$', get_recommendation, name='get_recommendation'),
     url(r'^$', searchpaper, name='search_paper'),
     path('', HomePageView.as_view(), name='home'),
     url(r'^(?P<pid>\d+)/preference/(?P<userpreference>\d+)/$', postpreference, name='postpreference'),
]
