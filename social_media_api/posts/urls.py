from .views import PostViewSet, CommentViewSet, FeedView
from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),]