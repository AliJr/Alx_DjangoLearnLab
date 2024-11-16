from django.http import HttpResponse
from .models import Book,Library
from django.views.generic.detail import DetailView
from django.shortcuts import render

def list_books(request):
    # Query all books with their related authors
    books = Book.objects.select_related('author').all()
    
    # Prepare a list of book titles and authors
    book_list = [f"{book.title} by {book.author.name}" for book in books]
    
    # Convert the list to a simple text response
    response_text = "\n".join(book_list)
    
    return HttpResponse(response_text, content_type="text/plain")



class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        # Fetch the default context
        context = super().get_context_data(**kwargs)
        # Add books related to the library
        context['books'] = self.object.books.all()
        return context

