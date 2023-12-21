from datetime import date, datetime
from django.db import models 

# Create your models here. 
class Author(models.Model): 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(primary_key=True) 

    def full_name(self): 
        return f'{self.first_name} {self.last_name}' 
    
    def __str__(self) -> str:
        return self.full_name()
    
class Tag(models.Model): 
    caption = models.CharField(max_length=100) 

    def __str__(self): 
        return self.caption

class Post(models.Model): 
    title = models.CharField(max_length=200) 
    summary = models.CharField(max_length=500) 
    image_name = models.CharField(max_length=500) 
    created_date = models.DateField(editable=False) 
    last_modified_date = models.DateField(editable=False) 
    content = models.CharField(max_length=3000)
    slug = models.SlugField(db_index=True, null=False, blank=False) 
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, 
                               to_field="email", db_column="email") 
    tags = models.ManyToManyField(Tag, related_name="tags")

    def save(self,*args, **kwargs):
        # storing creation date and modification date 
        current_time = datetime.today()

        if self.created_date is None: 
            self.created_date = current_time 

        self.last_modified_date = current_time 

        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title