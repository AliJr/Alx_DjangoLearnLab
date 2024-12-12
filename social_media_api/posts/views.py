from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import viewsets, views, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "content"]
    filterset_fields = ["author", "title", "content"]  # Fields we want to filter by

    def perform_create(self, serializer):
        # Set the author to the current user when creating a post
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["content"]
    filterset_fields = ["author", "content"]  # Fields we want to filter by

    def perform_create(self, serializer):
        # Set the author to the current user when creating a comment
        serializer.save(author=self.request.user)


class FeedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get(self, request):
        # Get the list of users that the current user is following
        following_users = request.user.following.all()
        # Retrieve posts from followed users, ordered by creation date
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
