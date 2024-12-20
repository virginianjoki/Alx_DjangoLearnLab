from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve a book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create a new book

    # Custom non-standard endpoints
    path('books/update/', BookUpdateView.as_view(), name='book-update-all'),  # Update multiple books (optional)
    path('books/delete/', BookDeleteView.as_view(), name='book-delete-all'),  # Delete multiple books (optional)

    # Standard RESTful endpoints
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  # Update a book by ID
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Delete a book by ID
]
