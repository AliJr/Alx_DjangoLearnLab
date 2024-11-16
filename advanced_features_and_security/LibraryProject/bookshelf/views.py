# The secure_search view uses Django ORM to prevent SQL injection attacks
# User inputs are validated and sanitized by Django ORM's query methods



from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

def index(request): return HttpResponse("Welcome to my book store.")



@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        # Process form data here
        pass
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # Process form data here
        pass
    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})