from django.conf.urls import url
from .views import searchpaper, get_recommendation, HomePageView, like_paper, dislike_paper
from django.urls import path

urlpatterns = [
     url(r'recommendation/$', get_recommendation, name='get_recommendation'),
     url(r'^$', searchpaper, name='search_paper'),
     path('', HomePageView.as_view(), name='home'),
     url(r'dislike/$', dislike_paper, name='dislike_paper'),
     url(r'like/$', like_paper, name='like_paper'),

]
