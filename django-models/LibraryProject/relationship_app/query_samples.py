from relationship_app.models import Author, Book, Librarian, Library

# Query all books by a specific author.
# List all books in a library.
# Retrieve the librarian for a library.
from relationship_app.models import Author, Library, Librarian

# Query 1: Get all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author) 
        return books
    except Author.DoesNotExist:
        return f"No author found with the name {author_name}"

# Query 2: List all books in a specific library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  
        return books
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"

# Query 3: Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"
    except Librarian.DoesNotExist:
        return f"No librarian found for the library {library_name}"