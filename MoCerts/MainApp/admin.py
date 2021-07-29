from django.contrib import admin
from .models import CustomUser, Certificate, PreviewSettings, ManualPosts, MainPagePost


class CertAdmin(admin.ModelAdmin):
    list_display = ('number', 'nominal', 'made_by', 'is_paid', 'owner',)
    list_display_links = ('number', 'nominal',)
    ordering = ['-published_date']
    list_filter = ('nominal', 'made_by', 'is_paid', 'owner',)
    search_fields = ('number', 'nominal', 'made_by', 'is_paid', 'owner',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'real_account', 'balance', 'telegram_id',)
    list_display_links = ('first_name', 'email',)
    ordering = ['-real_account']
    list_filter = ('real_account', 'balance',)
    search_fields = ('first_name', 'email', 'real_account', 'balance', 'telegram_id',)

class ManualAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'title',)
    list_display_links = ('index_number', 'title',)
    ordering = ['index_number']

class MainPagePostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'id', 'date_create',)
    list_display_links = ('headline',)
    ordering = ['-date_create']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Certificate, CertAdmin)
admin.site.register(PreviewSettings)
admin.site.register(ManualPosts, ManualAdmin)
admin.site.register(MainPagePost, MainPagePostAdmin)


admin.site.site_title = 'Панель администратора'
admin.site.site_header = 'Mosert Certificates'
