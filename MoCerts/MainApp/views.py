from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
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
        context['SignupForm'] = MySignupForm  # форма регистрации
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
    '''Страница выбора сертификата'''
    template_name = 'MainApp/select_certificate.html'

class CertificateDetail(DetailView):
    model = Certificate
    slug_field = "number"
    slug_url_kwarg = "number"
    context_object_name = 'certificate'
    template_name = 'MainApp/certificate.html'

    def get(self, *args, **kwargs):
        responsive = super().get(*args, **kwargs)
        if self.request.user != self.object.owner:
            '''если сертификат открыл другой польззователь, то отметить как получен'''
            self.object.is_received = True
            self.object.save()
        return responsive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_paid == False:
            context['need_pay'] = True
        if self.object.is_accept == False:
            context['need_accept'] = True
        if self.object.owner == self.request.user:
            context['owner_is_here'] = True
        if self.object.made_by == self.request.user:
            context['made_by'] = True

        return context


class MyCertificates(LoginRequiredMixin, ListView):
    '''Страница мои сертификаты'''
    context_object_name = 'queryset'
    template_name = 'MainApp/my_certificates.html'

    def get_queryset(self):
        '''отсортировать queryset по номиналам в списке'''
        certificates = Certificate.objects.filter(
            made_by=self.request.user,)
        nominals = [1, 5, 10, 20, 50, 100, 200, 300,]
        queryset = []
        for i in nominals:
            queryset.append([])
            for cert in certificates:
                if cert.nominal==i:
                    queryset[nominals.index(i)].append(cert)
        queryset = [x for x in queryset if x]
        print(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

   
@login_required
def create_certificate(request, nominal):
    '''Создать сертификат'''
    if request.method == 'GET':
        if Certificate.objects.filter(nominal=nominal, owner=request.user, is_accept=True):
            return HttpResponseRedirect(reverse('certificate',
                                                kwargs={'number': request.user.certificate.number}))

        number = datetime.today().strftime("%d%m%y%H%M%f")
        url = '{}/certificate/{}'.format(settings.HOST, number)

        user1_fullname = false_user()
        user2_fullname = false_user()
        user3_fullname = false_user()

        user1 = CustomUser.objects.create(username=user1_fullname[0] + user2_fullname[1], first_name=user1_fullname[0],
                                          last_name=user1_fullname[1],
                                          email=f'fakeuser1{number}@gmail.com',
                                          password=user2_fullname, real_account=False,)
        user2 = CustomUser.objects.create(username=user2_fullname[0] + user3_fullname[1], first_name=user2_fullname[0],
                                          last_name=user2_fullname[1],
                                          email=f'fakeuser2{number}@gmail.com',
                                          password=user3_fullname, real_account=False,)
        user3 = CustomUser.objects.create(username=user1_fullname[0] + user3_fullname[1], first_name=user3_fullname[0],
                                          last_name=user3_fullname[1],
                                          email=f'fakeuser3{number}@gmail.com',
                                          password=user1_fullname, real_account=False,)
        image_certificate = generate_certificate(
            nominal, number, user1, user2, user3)
        certificate = Certificate(number=number, url=url, nominal=nominal, user1=user1, user2=user2, user3=user3,
                                  certificate_image=image_certificate, owner=request.user,)
        certificate.save()
        cert_owner = request.user
        cert_owner.certificate = certificate
        cert_owner.save()
        return HttpResponseRedirect(reverse('certificate',
                                            kwargs={'number': request.user.certificate.number}))


@login_required
def pay_certificate(request, pk):
    '''оплата сертификата'''
    certificate = Certificate.objects.get(id=pk)
    if certificate.owner == request.user:
        if request.user.balance >= certificate.nominal:
            certificate.owner = None
            certificate.is_paid = True
            certificate.save()

            request.user.balance -= certificate.nominal
            request.user.save()

            user1 = certificate.user1
            if user1.real_account:
                user1.balance += certificate.nominal
                user1.save()
            else:
                if CustomUser.objects.filter(email=settings.MONEY_ADMIN['email']).exists():
                    money_admin = CustomUser.objects.get(email=settings.MONEY_ADMIN['email'])
                else:
                    money_admin = CustomUser.objects.create(username=settings.MONEY_ADMIN['username'], first_name=settings.MONEY_ADMIN['first_name'],
                                                            last_name=settings.MONEY_ADMIN['last_name'], email=settings.MONEY_ADMIN['email'],
                                                            password=settings.MONEY_ADMIN['password'],)
                money_admin.balance += certificate.nominal
                money_admin.save()   

            for i in range(0, 5):
                user1, user2, user3 = certificate.user2, certificate.user3, request.user
                number = datetime.today().strftime("%d%m%y%H%M%f")
                image_certificate = generate_certificate(
                    certificate.nominal, number, user1, user2, user3)
                url = '{}/certificate/{}'.format(settings.HOST, number)

                new_certificate = Certificate(number=number, url=url, nominal=certificate.nominal, user1=user1,
                                            user2=user2, user3=user3, certificate_image=image_certificate, 
                                            made_by=request.user, is_accept=False, owner=request.user,)
                new_certificate.save()

                                
            return HttpResponseRedirect(reverse('my_certificates'))
        else:
            messages.add_message(
                request, messages.ERROR, 'Недостаточно средств, пожалуйста, пополните баланс')
        return HttpResponseRedirect(reverse('profile'))


@login_required
def accept(request, pk):
    '''Подтвердить сертификат'''
    certificate = Certificate.objects.get(pk=pk)
    certificate.is_accept = True
    certificate.owner = request.user
    certificate.save()
    request.user.certificate = certificate
    request.user.save()
    return HttpResponseRedirect(reverse('certificate',
                                        kwargs={'number': certificate.number}))
