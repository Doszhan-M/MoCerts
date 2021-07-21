from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser, )


admin.site.site_title = 'Панель администратора'
admin.site.site_header = 'Mosert Certificates'
