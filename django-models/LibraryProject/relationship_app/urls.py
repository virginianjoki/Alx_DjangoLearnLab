from django.urls import path
from .views import BookListView, SignUpView,LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books

url_patterns = [
    path("", view=list_books, name='list_books'),
    path("", BookListView.as_view(template_name='relationship_app/list_books.html'), name = 'list'),
    path("", LibraryDetailView.as_view(template_name='relationship_app/library_detail.html'), name='library_detail'),
    path("", SignUpView, name = 'signup'),
    path("views.register", LoginView.as_view(template_name='registration/login.html', name = 'login')),
    path("views.register", LogoutView.as_view(template_name='registration/logout.html', name = 'logout')),
]