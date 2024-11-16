from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        # Use objects.filter to query related books
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return f"Author '{author_name}' not found."


# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return f"Library '{library_name}' not found."


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian  # Accesses the related librarian object
    except Library.DoesNotExist:
        return f"Library '{library_name}' not found."
    except Librarian.DoesNotExist:
        return f"Librarian for library '{library_name}' not found."


# Example usage (uncomment and run in Django shell or script):
# print(get_books_by_author("J.K. Rowling"))
# print(get_books_in_library("City Library"))
# print(get_librarian_for_library("City Library"))