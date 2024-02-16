from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView as DefaultLogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from .models import UserProfile

# Registration View


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Registration successful. You can now log in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Registration failed. Please correct the errors below.')
        return super().form_invalid(form)

# Login View


class LoginView(DefaultLoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('accounts:profile')

# Logout View


class LogoutView(DefaultLogoutView):
    next_page = reverse_lazy('accounts:login')

# Profile View


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(
            user=self.request.user)
        return context
