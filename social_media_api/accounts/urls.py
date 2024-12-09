from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterView, LoginView, UserProfileView

#router = DefaultRouter()
#router.register(r'users', views.UserView.as_view(), basename='user')



urlpatterns = [
    #path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]