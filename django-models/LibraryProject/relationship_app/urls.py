from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView  # Import default views


urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'), # Login view
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),# Logout view
    path('register/', views.register, name='register'),
]


