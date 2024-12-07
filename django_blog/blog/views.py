from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, ProfileForm
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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
