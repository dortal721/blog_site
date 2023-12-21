from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index_page'), 
    path('all-posts', views.all_posts, name='all_posts'),
    path('all_posts/<slug:slug>', views.single_post, name='single_post')
]