from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegistrationView, LoginView, UserView

#router = DefaultRouter()
#router.register(r'users', views.UserView.as_view(), basename='user')


urlpatterns = [
    #path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
]
