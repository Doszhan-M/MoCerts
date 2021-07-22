from django.contrib import admin
from .models import CustomUser, Certificate

admin.site.register(CustomUser)
admin.site.register(Certificate)


admin.site.site_title = 'Панель администратора'
admin.site.site_header = 'Mosert Certificates'
