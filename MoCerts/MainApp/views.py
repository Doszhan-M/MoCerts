from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import MyLoginForm, MySignupForm
from .models import CustomUser


class MainView(FormView):
    '''Главная страница'''
    template_name = 'Certificate/index.html'
    form_class = MyLoginForm

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['SignupForm'] = MySignupForm # форма регистрации
        return context


class UserProfile(LoginRequiredMixin, TemplateView):
    """кабинет пользователя"""
    model = CustomUser
    template_name = 'Users/profile.html'
    context_object_name = 'profile'
    login_url = '/'



