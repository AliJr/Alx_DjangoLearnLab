from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('title', 'author')

    # Add list filters for easy filtering
    list_filter = ('title', 'author')

    # Enable search capabilities
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)