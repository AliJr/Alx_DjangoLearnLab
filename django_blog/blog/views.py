from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, ProfileForm, CommentForm
from .models import Post, Comment
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "blog/register.html"


# Login View
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


# Logout View
def user_logout(request):
    logout(request)
    return redirect("home")


# Profile View
def profile(request):
    if request.method == "POST":
        # Update user details like email
        user = request.user
        user.email = request.POST.get("email")
        user.save()
    return render(request, "blog/profile.html", {"user": request.user})


def home(request):
    posts = Post.objects.all().order_by(
        "-published_date"
    )  # Get all posts, ordered by the published date
    return render(request, "blog/home.html", {"posts": posts})


# View for listing all blog posts
def posts(request):
    posts = Post.objects.all().order_by(
        "-published_date"
    )  # Fetch all posts ordered by published date (newest first)
    return render(request, "blog/posts.html", {"posts": posts})


@login_required
def edit_profile(request):
    profile = request.user  # Get the user's profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to the profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, "blog/edit_profile.html", {"form": form})


# List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5  # Optional: Limit the number of posts per page


# Show details of a single post
# Display post detail along with its comments
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


# Create a new post (only logged-in users can create)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically set the author
        return super().form_valid(form)

    success_url = reverse_lazy("post_list")  # Redirect to post list after creation


# Update an existing post (only the author can edit)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = (
            self.request.user
        )  # Ensure the post is still linked to the author
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only the author can update their post

    success_url = reverse_lazy("post_list")


# Delete a post (only the author can delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only the author can delete their post

    success_url = reverse_lazy("post_list")  # Redirect to post list after deletion



# Create a new comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        # Get the post using 'pk' from the URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])  # Use 'pk' here
        form.instance.author = self.request.user
        form.instance.post = post  # Associate the comment with the correct post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
# Edit an existing comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
    
    
# Delete an existing comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
    
    
# Search posts by title, content, or tags
def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()  # Ensure no duplicates from tags
    else:
        posts = Post.objects.all()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

# Display posts for a specific tag
def posts_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/tags.html', {'posts': posts, 'tag_name': tag_name})


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'  # Create this template to display posts by tag
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Override the default queryset to filter posts by tag.
        """
        tag_slug = self.kwargs.get('tag_slug')
        tag = Tag.objects.get(slug=tag_slug)  # Get the Tag object using the slug
        return Post.objects.filter(tags=tag)  # Return posts that are associated with the tag