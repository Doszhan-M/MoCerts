import os
import ast
from colorama import Fore, Style
from MoCerts.log_settings import log_settings


try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *


MONEY_ADMIN = {'username':'money', 'first_name':'MONEY_ADMIN', 'last_name':'money',
                'email':'money@gmail.com', 'password':'MONEY_ADMIN!'}



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    
    'MainApp',

    'easy_thumbnails',
    'modeltranslation',
    'embed_video',
    'ckeditor',
    'ckeditor_uploader',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.instagram',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MoCerts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Templates', BASE_DIR / 'Templates' / 'allauth',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

WSGI_APPLICATION = 'MoCerts.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_DIR = os.path.join(BASE_DIR, 'media/')
MEDIA_ROOT = MEDIA_DIR


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

THUMBNAIL_ALIASES = {
    '':
        {
            'my_certs_page': {'size': (182, 129), 'crop': 'smart'},
            'select_certs_page': {'size': (210, 150), 'crop': 'smart'}
        }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1


AUTH_USER_MODEL = 'MainApp.CustomUser'
ACCOUNT_ADAPTER = 'MainApp.adapter.MyAccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {'signup': 'MainApp.forms.MySignupForm', 'login': 'MainApp.forms.MyLoginForm'}
# ?????????????????? ?????????????????? ??????????????
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
try:
    with open(os.path.join(BASE_DIR, 'secret/EMAIL_HOST.txt'), 'r') as token:
        smtp = token.read()
    EMAIL_HOST = smtp  # ?????????? ?????????????? ?????????? ?????? ???????? ???????? ?? ?????? ????
    EMAIL_PORT = 587  # ???????? smtp ?????????????? ???????? ????????????????????
    with open(os.path.join(BASE_DIR, 'secret/EMAIL_HOST_USER.txt'), 'r') as token:
        email = token.read()
    EMAIL_HOST_USER = email  # ???????? ?????? ????????????????????????
    with open(os.path.join(BASE_DIR, 'secret/EMAIL_HOST_PASSWORD.txt'), 'r') as token:
        password = token.read()
    EMAIL_HOST_PASSWORD = password  # ???????????? ???? ??????????
    EMAIL_USE_TLS = True
    with open(os.path.join(BASE_DIR, 'secret/ADMINS.txt'), 'r') as token:
        admins = token.read()
    ADMINS = [ast.literal_eval(admins),] # ???????????????? email ????????????????????????????, ?????? ???????????????? ?????????????????? ?????? ??????????????
    SERVER_EMAIL = email
    DEFAULT_FROM_EMAIL = email  # ???????????????????????? ?????? ???????????????? email ?????????? ??????????????????????
    EMAIL_SUBJECT_PREFIX = '[Mosert] '
except FileNotFoundError:
    print(Fore.RED + '???? ?????????????? ?????????? ???????????????? ?????????????????? ??????????????')
    print(Style.RESET_ALL)


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



# ??????????????????????
LOGGING = log_settings

# ?????????????????? ckeditor
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_MAX_WIDTH = 200
CKEDITOR_CONFIGS={
  'default': {
    'width': '100%',
    'height': 400,
    'toolbar': 'Custom',
    'extraPlugins': ','.join([
      'codesnippet',
      'youtube'
    ]),
    'toolbar_Custom': [
      [
        'Bold',
        'Italic',
        'Underline'
      ],
      [
        'Font',
        'FontSize',
        'TextColor',
        'BGColor'
      ],
      [
        'NumberedList',
        'BulletedList',
        '-',
        'Outdent',
        'Indent',
        '-',
        'JustifyLeft',
        'JustifyCenter',
        'JustifyRight',
        'JustifyBlock'
      ],
      [
        'Link',
        'Unlink'
      ],
      [
        'Image',
        'Youtube',
        'RemoveFormat',
        'CodeSnippet',
        'Source',
      ]
    ],
    
  },
  
}