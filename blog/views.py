import datetime
from django.shortcuts import render 
from .models import Post


# Create your views here. 
def index(request): 
    latest_posts = Post.objects.all().order_by("created_date")
    
    return render(request, 'blog/index.html', {'latest_posts': latest_posts})

def all_posts(request):
    return render(request, 'blog/all-posts.html', {'posts': Post.objects.all()}) 

def single_post(request, slug): 
    cur_post = Post.objects.get(slug=slug) 
    
    return render(request, 'blog/post-detail.html', {'blog_data': cur_post})
