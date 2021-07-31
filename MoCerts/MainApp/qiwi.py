from .models import QiwiSecretKey


if QiwiSecretKey.objects.exists():
    QIWISECRET_KEY = QiwiSecretKey.objects.all()[0].secret_key
else:
    QiwiSecretKey.objects.create()
    QIWISECRET_KEY = QiwiSecretKey.objects.all()[0].secret_key


