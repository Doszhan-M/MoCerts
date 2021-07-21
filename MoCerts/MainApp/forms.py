from allauth.account.forms import LoginForm, SignupForm
from django.forms import ModelForm, TextInput, CharField
from .models import CustomUser


class MyLoginForm(LoginForm):

    def save(self, request):
        user = super(MyLoginForm, self).save(request)
        return user


class MySignupForm(SignupForm, ModelForm):

    first_name = CharField(
        label='Имя', widget=TextInput(attrs={'placeholder': 'Имя'}), required=True)
    last_name = CharField(
        label='Имя', widget=TextInput(attrs={'placeholder': 'Фамилия'}), required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',]

    def save(self, request):
        user = super(MySignupForm, self).save(request)
        return user