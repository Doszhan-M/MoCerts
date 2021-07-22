from django.urls import path
from .views import MainView, UserProfile, ManualView, SelectCertificate, create_certificate, my_certificates,\
     certificate, accept, pay_certificate


urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('manual/', ManualView.as_view(), name='manual'),

    path('certificates/', SelectCertificate.as_view(), name='select_certificate'),
    path('my_certificates', my_certificates, name='my_certificates'),
    path('create_certificate/<int:nominal>/', create_certificate, name='create_certificate'),
    path('certificate/<int:number>/', certificate, name='certificate'),
    path('accept/<int:pk>', accept, name='accept'),
    path('pay_certificate/<int:pk>', pay_certificate, name='pay_certificate'),
]
