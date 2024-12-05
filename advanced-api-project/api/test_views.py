from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        # Set up a user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password")
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2020, author=self.author
        )
        self.url = reverse("book-list")  # Assuming 'book-list' is the name of the ListView endpoint

    def test_create_book_authenticated(self):
        """
        Test the creation of a new book when authenticated
        """
        self.client.login(username="testuser", password="password")  # Authenticate user
        data = {"title": "New Book", "publication_year": 2023, "author": self.author.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication
        """
        data = {"title": "New Book", "publication_year": 2023, "author": self.author.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """
        Test updating a book when authenticated
        """
        self.client.login(username="testuser", password="password")
        data = {"title": "Updated Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.put(reverse("book-detail", args=[self.book.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book when authenticated
        """
        self.client.login(username="testuser", password="password")
        response = self.client.delete(reverse("book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        """
        Test filtering books by title
        """
        response = self.client.get(self.url + "?title=Test Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_author(self):
        """
        Test searching books by author
        """
        response = self.client.get(self.url + "?search=Test Author")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication year
        """
        Book.objects.create(
            title="Old Book", publication_year=1999, author=self.author
        )
        response = self.client.get(self.url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Old Book")
    
    def test_permission_check_on_update(self):
        """
        Test that only authenticated users can update a book
        """
        data = {"title": "Invalid Update", "publication_year": 2025, "author": self.author.id}
        response = self.client.put(reverse("book-detail", args=[self.book.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_permission_check_on_delete(self):
        """
        Test that only authenticated users can delete a book
        """
        response = self.client.delete(reverse("book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
