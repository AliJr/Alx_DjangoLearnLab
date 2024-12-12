from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from rest_framework import viewsets, views, permissions, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

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

class LikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        # check if user has already liked the post
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"detail": "Post already liked."}, status=status.HTTP_400_BAD_REQUEST)
        # Create a like
        Like.objects.get_or_create(post=post, user=request.user)
        # Create a notification
        Notification.objects.create(
            recipient = post.author, # recipient is the author of the post
            actor = request.user, # actor is the user who liked the post
            verb = "liked",
            target_content_type = ContentType.objects.get_for_model(Post),
            target_object_id = post.id,
            target = post,
        )
        
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)
    
class UnlikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # check if user has already liked the post
        like = Like.objects.filter(post=post, user=request.user)
        if not like.exists():
            return Response({"detail": "Post not liked."}, status=status.HTTP_400_BAD_REQUEST)
        
        Like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)