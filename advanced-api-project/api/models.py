from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author in the system.

    Attributes:
        name (str): The name of the author.
    """
    name = models.CharField(max_length = 100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete = models.CASCADE)

    

