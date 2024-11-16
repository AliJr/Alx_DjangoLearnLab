from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin

class BookAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('title', 'author', 'publication_date')

    # Add list filters for easy filtering
    list_filter = ('author', 'publication_date')

    # Enable search capabilities
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,  # Default UserAdmin fields
        (
            'Custom Fields',  # Add custom fields here
            {
                'fields': ('date_of_birth', 'profile_photo'),
            },
        ),
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom Fields',
            {
                'fields': ('date_of_birth', 'profile_photo'),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
