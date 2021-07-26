from django.core.management.color import color_style
from pathlib import Path
import logging
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent

class DjangoColorsFormatter(logging.Formatter):
    """вывод лога в разных цветах"""
    def __init__(self, *args, **kwargs):
        super(DjangoColorsFormatter, self).__init__(*args, **kwargs)
        self.style = self.configure_style(color_style())

    def configure_style(self, style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_INFO
        style.WARNING = style.HTTP_NOT_FOUND
        style.ERROR = style.ERROR
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

    def format(self, record):
        message = logging.Formatter.format(self, record)
        if sys.version_info[0] < 3:
            if isinstance(message, str):
                message = message.encode('utf-8')
        colorizer = getattr(self.style, record.levelname, self.style.HTTP_SUCCESS)
        return colorizer(message)


log_settings = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        # логгер для принтов
        '': {
            'handlers': ['console_log', 'common_file_log', 'mail_admins',],
            'level': 'INFO',
            'propagate': True
        },
        # отключить вывод в консоль логи джанго против дублирования
        'django': {
            'handlers': ['django_console_off',],
            'level': 'INFO',
            'propagate': True
        },

        'django.request': {
            'handlers': ['common_file_log',],
            'level': 'INFO',
            'propagate': True
        },

        'django.template': {
            'handlers': ['common_file_log',],
            'level': 'INFO',
            'propagate': True
        },

        'django.db.backends': {
            'handlers': ['common_file_log',],
            'level': 'INFO',
            'propagate': True
        },
        # security необходим, он идет в обход django
        'django.security.*': {
            'handlers': ['console_log', ],
            'level': 'INFO',
            'propagate': True
        },

        'celery': { # это настройка не работает TODO
            'handlers': ['celery_handler'],
            'level': 'INFO',
            'propagate': True,
        },

    },

    'handlers': {
        # выключить django вывод в консоль
        'django_console_off': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
            'formatter': 'colored',
        },

        'console_log': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },

        'common_file_log': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/common_log.log'),
            'when': 'W0',
            'backupCount': 10,
            'formatter': 'colored',
        },

        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'colored',
            'include_html': True,
            'email_backend': 'allauth.account.auth_backends.AuthenticationBackend',
        },
        
        'celery_handler': { # это настройка не работает TODO
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/celery_log.log'),

        }
    },

    'formatters': {  
        'colored': {
            '()': DjangoColorsFormatter,
            'format': '[%(asctime)s] - %(levelname)s - %(message)s - %(name)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
         },

    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

}
