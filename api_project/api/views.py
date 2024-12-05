from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    #apply permissions
    permission_classes = [IsAuthenticated]          
