from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django_filters import filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import django_filters
from rest_framework.filters import SearchFilter
from django_filters import rest_framework

# Define a filter class for Book model
class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    author = django_filters.CharFilter(lookup_expr='icontains', label='Author contains')
    publication_year = django_filters.NumberFilter(lookup_expr='exact', label='Publication Year')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# ListView - Retrieve all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    #filterset_class = BookFilter
    search_fields = ['title', 'author']  # Fields to search
    ordering_fields = ['title', 'publication_year']  # Fields that can be ordered
    ordering = ['title']  # Default ordering
    permission_classes = [IsAuthenticatedOrReadOnly]  # Optional: Restrict based on authentication

# DetailView - Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'  # Specify the field for ID lookup (default is 'pk')
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users


# CreateView - Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

# UpdateView - Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update


# DeleteView - Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
