#Import the Book model
from bookshelf.models import Book

#delete book
retrieved_book.delete()

#Confirm deletion
books = Book.objects.all()
print(books)
