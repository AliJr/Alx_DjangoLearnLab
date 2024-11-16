from django.http import HttpResponse
from .models import Book,Library
from django.views.generic.detail import DetailView
from django.shortcuts import render

def list_books(request):
    # Fetch all books with their authors
    books = Book.objects.select_related('author').all()
    # Render the template with the books context
    return render(request, 'relationship_app/list_books.html', {'books': books})



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

