from django.db import models

# Author model stores information about authors.
# It has a name field that is unique for each author.
# Books can be related to an author through a ForeignKey relationship.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

# Book model stores information about books.
# It includes a title, a publication year, and a ForeignKey to the Author model.
# The ForeignKey defines a many-to-one relationship from Book to Author.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)