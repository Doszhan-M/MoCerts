from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from .models import CustomUser
from django.urls import reverse_lazy


class MainView(FormView, TemplateView):
    template_name = 'Certificate/index.html'
    form_class = MyLoginForm





class UserProfile(LoginRequiredMixin, TemplateView):
    """кабинет пользователя"""
    model = CustomUser
    template_name = 'Users/profile.html'
    context_object_name = 'profile'
    login_url = '/'



