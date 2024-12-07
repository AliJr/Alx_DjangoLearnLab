from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, ProfileForm
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


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
