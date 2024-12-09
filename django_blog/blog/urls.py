from .views import HomeView, RegisterView, ProfileView
from django.urls import path
from . import views


urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('register/',views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    #  # path urls for CRUD actions on posts
    # path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    # path('post/list-view/', views.PostListView.as_view(), name='post-list'),
    # path('post/<int:pk>/detail/', views.PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # path urls for CRUD actions on comments
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('post/comment-list-view/', views.CommentListView.as_view(), name='comment-list'),
    # path('post/<int:pk>/comment-detail/', views.CommentDetailView.as_view(), name='post-comment-detail'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='post-comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='post-comment-delete'),

    # path urls to filter posts by tags
    path('tag/<str:tag_name>/', views.post_by_tag, name='post-by-tag'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),

    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]