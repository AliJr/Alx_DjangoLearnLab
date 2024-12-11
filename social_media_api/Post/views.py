from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, filters, authentication
from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
# Create your views here.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    def perform_create(self, serializer):
        # Set the author to the current user when creating a post
        serializer.save(author=self.request.user)
    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['author','content']
    def perform_create(self, serializer):
        # Set the author to the current user when creating a comment
        serializer.save(author=self.request.user)