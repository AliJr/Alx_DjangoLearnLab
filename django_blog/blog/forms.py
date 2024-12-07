from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Comment
from taggit.forms import TagWidget


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture']
        
        
class PostForm(forms.ModelForm):
    # This will be a CharField because we will handle the tags as a comma-separated string
    tags = forms.CharField(
        max_length=255, 
        required=False, 
        help_text="Enter tags separated by commas.", 
        widget=TagWidget()  # Use TagWidget to handle the tags
    )
    class Meta:
        model = Post
        fields = ['title', 'content']
        
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            return tag_list
        return []
    
    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.request.user  # Automatically set the author to the logged-in user
        if commit:
            post.save()
        return post
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 4})