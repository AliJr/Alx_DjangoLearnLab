from django.contrib.auth import get_user_model
from .models import Post, Comment
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author']
        read_only_fields = ['author', 'created_at', 'updated_at']
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta: 
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'author', 'post']
        read_only_fields = ['author','created_at', 'updated_at']