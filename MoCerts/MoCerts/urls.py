from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static # нужно прописать путь статика для отабражения изображении

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('', include('MainApp.urls')),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)