from .models import Comment  
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['user_name', 'user_email', 'content'] 
        labels = {
            'user_name': 'Your Name', 
            'user_email': 'Your Email', 
            'content': 'Your Comment'
        }