from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from rest_framework import viewsets, views, permissions, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

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


class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Use get_object_or_404 to retrieve the post or return 404 if not found
        post = get_object_or_404(Post, pk=pk)

        user = request.user

        # Prevent the user from liking a post multiple times
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "You already liked this post."}, status=400)

        # Create the like
        Like.objects.create(user=user, post=post)

        # Create a notification for the post author
        notification = Notification(
            recipient=post.author,
            actor=user,
            verb="liked",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )
        notification.save()

        return Response({"detail": "Post liked successfully."})

class UnlikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Use get_object_or_404 to retrieve the post or return 404 if not found
        post = get_object_or_404(Post, pk=pk)

        user = request.user

        # Prevent the user from unliking a post they haven't liked
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=400)

        # Remove the like
        like.delete()

        return Response({"detail": "Post unliked successfully."})