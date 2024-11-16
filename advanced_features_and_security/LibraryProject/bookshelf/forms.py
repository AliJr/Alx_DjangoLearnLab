# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'genre']

    # Custom validation can be added here if necessary
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13:  # Example validation for ISBN length
            raise forms.ValidationError('ISBN must be 13 characters long')
        return isbn
