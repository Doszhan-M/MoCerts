from datetime import datetime
import logging

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy, reverse
from django.conf import settings

from .names.names_generator import false_user
from .certificates.certificate_generator import generate_certificate
from .forms import MyLoginForm, MySignupForm, UserForm
from .qiwi import QIWISECRET_KEY
from .models import CustomUser, Certificate, ManualPosts, MainPagePost

logger = logging.getLogger(__name__)


class UserBalance(LoginRequiredMixin, TemplateView):
    """страница баланса"""
    template_name = 'MainApp/userbalance.html'
    success_url = reverse_lazy('profile')
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(QIWISECRET_KEY)
        # context['SignupForm'] = MySignupForm  # форма регистрации
        return context


class AuthorizationForms(FormView):
    """формы для авторизации и регистрации через header"""
    form_class = MyLoginForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SignupForm'] = MySignupForm  # форма регистрации
        return context


class MainView(AuthorizationForms, ListView):
    '''Главная страница'''
    model = MainPagePost
    context_object_name = 'posts'
    ordering = ('-date_create')
    template_name = 'MainApp/index.html'


class PostDetail(AuthorizationForms, DetailView):
    '''Страница поста подробнее'''
    model = MainPagePost
    context_object_name = 'post'
    template_name = 'MainApp/postdetail.html'


class UserProfile(LoginRequiredMixin, UpdateView):
    """кабинет пользователя"""
    model = CustomUser
    context_object_name = 'user'
    template_name = 'MainApp/profile.html'
    form_class = UserForm
    success_url = reverse_lazy('profile')
    login_url = '/accounts/login/'

    def get_object(self,):
        obj = CustomUser.objects.get(first_name=self.request.user)
        return obj
    
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        messages.add_message(
                self.request, messages.INFO, 'Изменения сохранены')
        return super().post(request, *args, **kwargs)


class ManualView(AuthorizationForms, ListView):
    '''Страница инструкции'''
    model = ManualPosts
    context_object_name = 'manuals'
    template_name = 'MainApp/manual.html'
    ordering = 'index_number'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if not self.request.is_secure():
    #         logger.error(f'self.request.is_secure() {self.request.is_secure()}')
    #     return context


class SelectCertificate(AuthorizationForms, TemplateView):
    '''Страница выбора сертификата'''
    template_name = 'MainApp/select_certificate.html'


class CertificateDetail(AuthorizationForms, DetailView):
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
        context['host'] = settings.HOST
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
        nominals = [1, 5, 10, 20, 50, 100, 200, 500,]
        queryset = []
        for i in nominals:
            queryset.append([])
            for cert in certificates:
                if cert.nominal==i:
                    queryset[nominals.index(i)].append(cert)
        queryset = [x for x in queryset if x]
        return queryset


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
            certificate.paid_by_user = request.user
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
