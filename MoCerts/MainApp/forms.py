import re
from allauth.account.forms import LoginForm, SignupForm
from django.forms import ModelForm, TextInput, CharField, EmailInput, FileInput, IntegerField, NumberInput
from django.core.exceptions import ValidationError
from django import forms
from .models import CustomUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class DepositForm(forms.Form):
    '''форма пополнения'''
    amount = IntegerField(label='Сумма пополнения', widget=NumberInput(attrs={'placeholder': 'сумма $'}),\
        validators=[MinValueValidator(1),])

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 1


class WithdrawalForm(forms.Form):
    '''форма вывода средств'''
    
    withdrawal_amount = IntegerField(label='Сумма вывода', widget=NumberInput(attrs={'placeholder': 'сумма $'}),\
        validators=[MinValueValidator(1),])
    qiwi_wallet = CharField(
        label='Qiwi кошелек', widget=TextInput(attrs={'placeholder': 'номер кошелька'}), required=True)

    def __init__(self, *args, **kwargs):
        super(WithdrawalForm, self).__init__(*args, **kwargs)
        self.fields['withdrawal_amount'].widget.attrs['min'] = 1

    


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

        fields = ['first_name', 'last_name', 'email', 'photo',]

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
        }