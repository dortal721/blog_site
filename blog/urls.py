from django.urls import path 
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'), 
    path('all-posts', views.AllPostsView.as_view(), name='all_posts'),
    path('all_posts/<slug:slug>', views.SinglePostView.as_view(), name='single_post')
]