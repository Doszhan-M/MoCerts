from allauth.account.forms import LoginForm, SignupForm
from django.forms import ModelForm, TextInput, CharField, EmailInput, FileInput
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


class UserForm(ModelForm):
    """Модельная форма редактировать профиль"""

    class Meta:
        model = CustomUser

        fields = ['first_name', 'last_name', 'email', 'photo', 'balance',]

        labels = {'first_name': 'Имя',
                    'last_name': 'Фамилия', 'email': 'Email', 'photo': 'Аватар', }

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:20ch; background-color: transparent; border: none; font-size: 22px;',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:20ch; background-color: transparent; border: none; font-size: 22px;',
            }),
            'email': EmailInput(attrs={
                'multiple class': 'form-control',
                'style': 'width:20ch; background-color: transparent; border: none; font-size: 22px;',
            }),
            'photo': FileInput(attrs={
                'class': 'form-control',
                'style': 'width:30ch; border: none; font-size: 19px;',
            }),
            'balance': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'width:20ch; background-color: transparent; border: none; font-size: 22px;',
            }),
        }