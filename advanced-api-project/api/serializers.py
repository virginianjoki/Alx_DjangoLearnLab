from rest_framework import serializers
from .models import Book,Author
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields of the Book model

    def validate_published_date(self, value):
        #check that the published_date is not in the future.

        if value > date.today():
            raise serializers.ValidationError("The publication date cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name','books']