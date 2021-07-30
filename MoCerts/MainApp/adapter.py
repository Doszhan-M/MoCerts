from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser
from django.urls import reverse_lazy


# функция переопределения редиректов allauth
class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = reverse_lazy('main_page')
        return path

    def get_logout_redirect_url(self, request):
        path = reverse_lazy('main_page')
        return path

    def get_signup_redirect_url(self, request):
        path = reverse_lazy('main_page')
        return path