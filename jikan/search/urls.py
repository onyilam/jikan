from django.conf.urls import url
from . import views
from django.urls import path, re_path

urlpatterns = [
     url(r'recommendation/$', views.get_recommendation, name='get_recommendation'),
     url(r'^$', views.searchpaper, name='search_paper'),
     url(r'event/(?P<event_pk>\d+)/comment', views.add_comment_to_event, name='add_comment_to_event'),
     url(r'show_like/$', views.show_paper_likes, name='show_paper_likes'),
     url(r'like/$', views.like_paper, name='like_paper'),
     url(r'event/react', views.react_event, name='react_event'),
     path('paper/<int:pk>/', views.paper_detail, name='paper_detail'),
     url(r'^load/', views.load_paper, name='load_paper'),
     url(r'^edit/(?P<pk>\d+)/', views.edit_paper, name='edit_paper'),
     url(r'^load_user/', views.load_user, name='load_user'),
     url(r'^edit_user/(?P<pk>\d+)/', views.edit_user, name='edit_user'),
     url(r'^event/', views.add_event, name='add_event'),
     url(r'^post_event/(?P<pk>\d+)/', views.post_event, name='post_event'),
     url(r'^edit_event/', views.edit_event, name='edit_event'),
     url(r'^remove_paper/(?P<pk>\d+)/', views.remove_paper, name='remove_paper'),
     url(r'^remove_event/(?P<pk>\d+)/', views.remove_event, name='remove_event'),
     url(r'^ajax_calls/search/', views.autocompletePaper),
     path('profile/<int:pk>/', views.view_user, name="view_user"),
     path('', views.HomePageView.as_view(), name='home'),
     url(r'addpaper/$', views.add_paper, name='add_paper'),
]
