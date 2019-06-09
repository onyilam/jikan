from django.conf.urls import url
from .views import searchpaper, get_recommendation, HomePageView, like_paper, paper_detail, add_comment_to_paper, add_paper, PaperCreateView
from django.urls import path

urlpatterns = [
     url(r'recommendation/$', get_recommendation, name='get_recommendation'),
     url(r'^$', searchpaper, name='search_paper'),
     path('', HomePageView.as_view(), name='home'),
     url(r'like/$', like_paper, name='like_paper'),
     #url(r'add/$', add_paper, name='add_paper'),
     path('add/', PaperCreateView.as_view(), name='add_paper'),
     path('paper/<int:pk>/', paper_detail, name='paper_detail'),
     path('paper/<int:pk>/comment/', add_comment_to_paper, name='add_comment_to_paper'),

]
