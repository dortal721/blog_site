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

def is_post_saved(request, post_obj: Post): 
    stored_posts = request.session.get('stored_posts') 

    if stored_posts is None: 
        return False 
    
    return post_obj.id in stored_posts

class SinglePostView(View):

    def get(self, request, slug): 
        cur_post = Post.objects.get(slug=slug) 
    
        return render(request, 'blog/post-detail.html', 
                      {'blog_data': cur_post, 
                       'comment_form': CommentForm(), 
                       'comments': cur_post.comments.all().order_by("-id"), 
                       'is_saved': is_post_saved(request, cur_post)})
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        cur_post = Post.objects.get(slug=slug)

        if comment_form.is_valid(): 
            cur_comment = comment_form.save(commit=False)
            
            # assigning post id by slug 
            cur_comment.post_id = cur_post 

            cur_comment.save()

            # redirecting a GET request to the original page 
            return HttpResponseRedirect(reverse("single_post", args=[slug])) 
        
        # TODO: add is_saved to dictionary, and unify to use less code
        return render(request, 'blog/post-detail.html', 
                          {'blog_data': cur_post, 
                           'comment_form': comment_form, 
                           'comments': cur_post.cur_post.comments.all().order_by("-id")}) 
    
class ReadLaterView(View):
    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        # updating post to saved list 
        cur_post_id = int(request.POST['post_id'])

        if stored_posts is None: 
            stored_posts = [cur_post_id] 
        elif cur_post_id not in stored_posts: 
            stored_posts.append(cur_post_id) 
        else: 
            stored_posts.remove(cur_post_id)
            
        request.session['stored_posts'] = stored_posts
        cur_post_obj = Post.objects.get(id=cur_post_id)

        # redirecting a GET request to post page
        return HttpResponseRedirect(reverse('single_post', args=[cur_post_obj.slug]))
    

class SavedPostsView(View):
    def get(self, request): 
        # obtaining posts stored by the user 
        stored_posts_ids = request.session.get("stored_posts")

        # if None - output empty list 
        if stored_posts_ids is None: 
            return render(request, 'blog/saved-posts.html', 
                          {'posts': None}) 
        
        # if not None, but still empty - output empty list 
        if not len(stored_posts_ids): 
            return render(request, 'blog/saved-posts.html', 
                          {'posts': None}) 
        
        # otherwise - output full list 
        stored_posts = Post.objects.filter(id__in=stored_posts_ids)

        return render(request, 'blog/saved-posts.html', 
                          {'posts': stored_posts})

            

            

