from django.conf.urls import url
from .views import searchpaper, get_recommendation

urlpatterns = [
     url(r'^$', searchpaper, name='search_paper'),
     url(r'recommendation/', get_recommendation, name='get_recommendation'),
]
