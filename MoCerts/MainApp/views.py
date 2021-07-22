from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.conf import settings

from .forms import MyLoginForm, MySignupForm
from .models import CustomUser, Certificate

from .names.names_generator import false_user
from .certificates.certificate_generator import generate_certificate


class MainView(FormView):
    '''Главная страница'''
    template_name = 'MainApp/index.html'
    form_class = MyLoginForm

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['SignupForm'] = MySignupForm # форма регистрации
        return context


class UserProfile(LoginRequiredMixin, TemplateView):
    """кабинет пользователя"""
    model = CustomUser
    template_name = 'MainApp/profile.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(email=self.request.user.email)
        return context


class ManualView(TemplateView):
    '''Страница инструкции'''
    template_name = 'MainApp/manual.html'


class SelectCertificate(TemplateView):
    template_name = 'MainApp/select_certificate.html'


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(made_by=request.user)
    context = {'certificates_1': [],
               'certificates_5': [],
               'certificates_10': [],
               'certificates_20': [],
               'certificates_50': [],
               'certificates_100': [],
               'certificates_200': [],
               'certificates_500': []}
    for cert in certificates:
        if cert.nominal == 1:
            context['certificates_1'].append(cert)
        elif cert.nominal == 5:
            context['certificates_5'].append(cert)
        elif cert.nominal == 10:
            context['certificates_10'].append(cert)
        elif cert.nominal == 20:
            context['certificates_20'].append(cert)
        elif cert.nominal == 50:
            context['certificates_50'].append(cert)
        elif cert.nominal == 100:
            context['certificates_100'].append(cert)
        elif cert.nominal == 200:
            context['certificates_200'].append(cert)
        elif cert.nominal == 500:
            context['certificates_500'].append(cert)
    return render(request, template_name='MainApp/my_certificates.html', context=context)


# @login_required
def create_certificate(request, nominal):
    if request.method == 'GET':
        if request.user.certificate:
            return HttpResponseRedirect(reverse('certificate',
                                                kwargs={'number': request.user.certificate.number}))
        number = datetime.today().strftime("%d%m%y%H%M%f")
        url = '{}/certificate/{}'.format(settings.HOST, number)

        user1_fullname = false_user()
        user2_fullname = false_user()
        user3_fullname = false_user()

        print('number', number)
        print(user1_fullname, user2_fullname, user3_fullname)

        user1 = CustomUser.objects.create(username=user1_fullname[0] + user2_fullname[1], first_name=user1_fullname[0],
                        last_name=user1_fullname[1],
                        email=f'fakeuser1{number}@gmail.com',
                        password=user2_fullname)
        user2 = CustomUser.objects.create(username=user2_fullname[0] + user3_fullname[1], first_name=user2_fullname[0],
                        last_name=user2_fullname[1],
                        email=f'fakeuser2{number}@gmail.com',
                        password=user3_fullname)
        user3 = CustomUser.objects.create(username=user1_fullname[0] + user3_fullname[1], first_name=user3_fullname[0],
                        last_name=user3_fullname[1],
                        email=f'fakeuser3{number}@gmail.com',
                        password=user1_fullname)
        image_certificate = generate_certificate(nominal, number, user1, user2, user3)
        certificate = Certificate(number=number, url=url, nominal=nominal,
                                  user1=user1, user2=user2, user3=user3, certificate_image=image_certificate)
        certificate.save()
        mycertuser = request.user
        mycertuser.certificate = certificate
        mycertuser.save()
        return HttpResponseRedirect(reverse('certificate',
                                            kwargs={'number': request.user.certificate.number}))


@login_required
def certificate(request, number):
    mycertuser = request.user
    certificate = mycertuser.certificate
    if certificate and number == mycertuser.certificate.number:
        context = {'certificate': certificate, 'transfer': True}
        return render(request, template_name='MainApp/certificate.html', context=context)
    certificate = Certificate.objects.get(number=number)
    if certificate.made_by == mycertuser:
        context = {'certificate': certificate}
        return render(request, template_name='MainApp/certificate.html', context=context)
    if certificate.status != 'NONE':
        context = {'certificate': certificate}
        return render(request, template_name='MainApp/certificate.html', context=context)
    context = {'certificate': certificate, 'accept': True}
    return render(request, template_name='MainApp/certificate.html', context=context)                                     


@login_required
def accept(request, pk):
    certificate = Certificate.objects.get(pk=pk)
    certificate.status = 'RECEIVED'
    certificate.save()
    request.user.certificate = certificate
    request.user.save()
    return HttpResponseRedirect(reverse('certificate',
                                        kwargs={'number': certificate.number}))


@login_required
def pay_certificate(request, pk):
    if request.user.certificate.pk == pk:
        certificate = request.user.certificate
        if request.user.balance >= certificate.nominal:
            request.user.balance -= certificate.nominal
            certificate.payed = True
            certificate.status = 'PAID'
            certificate.save()
            request.user.certificate = None
            for i in range(0, 5):
                certificate.user1.balance += certificate.nominal
                user1, user2, user3 = certificate.user2, certificate.user3, request.user
                number = datetime.today().strftime("%d%m%y%H%M%f")
                image_certificate = generate_certificate(certificate.nominal, number, user1, user2, user3)
                url = '{}/certificate/{}'.format(settings.HOST, number)
                new_certificate = Certificate(number=number, url=url, nominal=certificate.nominal,
                                              user1=user1, user2=user2, user3=user3,
                                              certificate_image=image_certificate)
                new_certificate.made_by = request.user
                new_certificate.save()
            request.user.save()
            return HttpResponseRedirect(reverse('my_certificates'))
        else:
            return HttpResponseRedirect(reverse('certificate', kwargs={'number': certificate.number}))
    return HttpResponseNotFound('<h1>Page not found</h1>')                                        