from django.shortcuts import render, redirect
from .models import User,Post,Profile
from django.views.generic import TemplateView,CreateView,DetailView,ListView,UpdateView,DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import PostForm

# Create your views here.

class HomeView(TemplateView):
    template_name = "blog/base.html"

class RegisterView(CreateView):
    template_name = 'blog/register.html'  
    form_class = CustomUser
    success_url = reverse_lazy('login')  

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        #Fetch the profile for the currently logged-in user
        return Profile.objects.get(user = self.request.user)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST['email']
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')       

# CRUD Views opertions on POSTS by users
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        results = Post.objects.none()
    return render(request, 'blog/search_results.html', {'result': results})

def post_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.posts.all()
    return render(request, 'blog/post-by-tag.html', {'tag': tag, 'posts': posts})

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post-list-by-tag.html'  # Create this template
    context_object_name = 'posts'
    paginate_by = 5  # Optional: for pagination

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        # Allow only the author of the post to delete it
        post = self.get_object()  # Get the current post instance
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        # Allow only the author of the post to delete it
        post = self.get_object()  # Get the current post instance
        return self.request.user == post.author

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    fields = ['title', 'content', 'tags']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Set the author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the list view after successful creation
        return reverse_lazy('post-list')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# CRUD Operation Views on Comments

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['post','content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        # Set the author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the list view after successful creation
        return reverse_lazy('comment-list')
    

class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'blog/post_comments.html'


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        # Allow only the author of the comment to delete it
        comment = self.get_object()  # Get the current comment instance
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy("post_list")
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        # Allow only the author of the comment to delete it
        comment = self.get_object()  # Get the current comment instance
        return self.request.user == comment.author

