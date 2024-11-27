from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, Author
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create an author
        self.author = Author.objects.create(name="Test Author")
        
        # Create a user and get an authentication token
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        
        # Create a book object for CRUD testing
        self.book_data = {
            "title": "Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        self.book = Book.objects.create(**self.book_data)
        
        # Define API endpoint URLs
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book.id])

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

def test_create_book(self):
    response = self.client.post(self.book_list_url, self.book_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], self.book_data['title'])
    self.assertEqual(response.data['author']['name'], self.author.name)
    self.assertEqual(response.data['publication_year'], self.book_data['publication_year'])

def test_read_book(self):
    response = self.client.get(self.book_detail_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], self.book.title)
    self.assertEqual(response.data['author']['name'], self.author.name)

def test_update_book(self):
    updated_data = {"title": "Updated Test Book", "publication_year": 2025}
    response = self.client.put(self.book_detail_url, updated_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], updated_data['title'])
    self.assertEqual(response.data['publication_year'], updated_data['publication_year'])
def test_delete_book(self):
    response = self.client.delete(self.book_detail_url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # Verify that the book is deleted
    response = self.client.get(self.book_detail_url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_filter_books_by_author(self):
    response = self.client.get(self.book_list_url, {'author': self.author.id})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['author']['name'], self.author.name)

def test_search_books(self):
    response = self.client.get(self.book_list_url, {'search': 'Test Book'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreater(len(response.data), 0)
    self.assertIn('Test Book', [book['title'] for book in response.data])

def test_order_books_by_title(self):
    # Create another book with different title for ordering test
    Book.objects.create(title="Another Book", author=self.author, publication_year=2024)
    
    response = self.client.get(self.book_list_url, {'ordering': 'title'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data[0]['title'], "Another Book")

def test_create_book_without_authentication(self):
    response = self.client.post(self.book_list_url, self.book_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_create_book_with_authentication(self):
    self.authenticate()  # Authenticate the user
    response = self.client.post(self.book_list_url, self.book_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

def test_update_book_without_authentication(self):
    response = self.client.put(self.book_detail_url, {"title": "Updated Book"}, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_update_book_with_authentication(self):
    self.authenticate()  # Authenticate the user
    response = self.client.put(self.book_detail_url, {"title": "Updated Book"}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
