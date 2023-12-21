from django.contrib import admin 
from .models import Post, Author, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin): 
    readonly_fields = ("created_date", "last_modified_date", )
    prepopulated_fields = {"slug": ("title",)} 

admin.site.register(Post, PostAdmin) 
admin.site.register(Author)
admin.site.register(Tag)