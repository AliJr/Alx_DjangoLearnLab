from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Author, Book

class BookAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a user and generate a token for token-based authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        
        # Create an author and a book
        self.author = Author.objects.create(name="Test Author")
        self.book_data = {
            "title": "Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        self.book = Book.objects.create(**self.book_data)
        
        # Define API endpoint URLs
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book.id])

    def test_create_book_with_token(self):
        # Authenticate using token authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create a new book
        response = self.client.post(self.book_list_url, self.book_data, format='json')
        
        # Check if the book was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])

    def test_list_books_with_token(self):
        # Authenticate using token authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Retrieve the list of books
        response = self.client.get(self.book_list_url)
        
        # Check if the response contains the correct data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book should be present

    def test_update_book_with_token(self):
        # Authenticate using token authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Updated book data
        updated_data = {
            "title": "Updated Book Title",
            "author": self.author.id,
            "publication_year": 2024
        }
        
        # Update the book
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        
        # Check if the book was updated successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_delete_book_with_token(self):
        # Authenticate using token authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Delete the book
        response = self.client.delete(self.book_detail_url)
        
        # Check if the book was deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Session-based authentication tests (Alternative, if using session authentication)
    def test_create_book_with_session(self):
        # Log in the user using session authentication
        self.client.login(username='testuser', password='password')
        
        # Create a new book
        response = self.client.post(self.book_list_url, self.book_data, format='json')
        
        # Check if the book was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])

    def test_list_books_with_session(self):
        # Log in the user using session authentication
        self.client.login(username='testuser', password='password')
        
        # Retrieve the list of books
        response = self.client.get(self.book_list_url)
        
        # Check if the response contains the correct data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book should be present
