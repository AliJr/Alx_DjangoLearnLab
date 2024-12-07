from django.views.generic import CreateView, TemplateView
from .forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url= reverse_lazy('login')
    template_name = 'blog/register.html'
    
    
class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'blog/profile.html'
    
        # Add user data to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Pass the logged-in user to the template
        return context