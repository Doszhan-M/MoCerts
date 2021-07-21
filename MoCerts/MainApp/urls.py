from django.urls import path
from .views import MainView, UserProfile, PasswordsChangeView


urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('change_password', PasswordsChangeView.as_view(template_name='MainApp/change_password.html'), name='changepassword'),

]