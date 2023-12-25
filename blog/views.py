import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render 
from django.views.generic import ListView
from django.views import View 
from django.http import HttpResponseRedirect 
from django.urls import reverse

from .models import Post 
from .forms import CommentForm

class IndexView(ListView): 
    template_name = 'blog/index.html' 
    model = Post 
    ordering = ["-created_date"]
    context_object_name = "latest_posts"

    def get_queryset(self):
        return super().get_queryset()[:3]
    
class AllPostsView(ListView): 
    template_name = 'blog/all-posts.html' 
    model = Post 
    ordering = ["-created_date"] 
    context_object_name = "posts" 

class SinglePostView(View): 
    def get(self, request, slug): 
        cur_post = Post.objects.get(slug=slug)
    
        return render(request, 'blog/post-detail.html', 
                      {'blog_data': cur_post, 
                       'comment_form': CommentForm(), 
                       'comments': cur_post.comments.all()})
    
    def post(self, request, slug): 
        comment_form = CommentForm(request.POST) 

        if comment_form.is_valid(): 
            cur_comment = comment_form.save(commit=False)
            
            # assigning post id by slug 
            cur_post = Post.objects.get(slug=slug) 
            cur_comment.post_id = cur_post 

            cur_comment.save() 

            # redirecting a GET request to the original page 
            return HttpResponseRedirect(reverse("single_post", args=[slug]))

        return render(request, 'blog/post-detail.html', 
                          {'blog_data': cur_post, 
                           'comment_form': comment_form, 
                           'comments': cur_post.cur_post.comments.all()})