from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView
from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike'),]


