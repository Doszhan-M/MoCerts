import logging
import time
from celery import shared_task
from pyqiwip2p import QiwiP2P
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Deposit, CustomUser


logger = logging.getLogger(__name__)


@shared_task
def check_payment_status(QIWI_PRIV_KEY, bill_id, lifetime, email, amount):
    '''проверить статус выставленного счета'''
    process_step = 0
    while process_step < lifetime:
        logger.info('проверить статус выставленного счета ' + bill_id)
        # подключиться к сервису qiwi
        p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
        status = p2p.check(bill_id=bill_id).status
        print('process_step', lifetime - process_step)

        if status == 'WAITING':
            logger.info('if статус счета ' + status)
            process_step += 1
            if lifetime - process_step == 1:
                status = 'EXPIRED'

        if status == 'PAID':
            logger.info('if статус счета ' + status)
            transaction = Deposit.objects.get(bill_id=bill_id)
            transaction.status = 2
            transaction.save()

            cur_user = CustomUser.objects.get(email=email)
            cur_user.balance += amount
            cur_user.save()
            process_step += lifetime

        if status == 'EXPIRED':
            logger.info('if статус счета ' + status)
            transaction = Deposit.objects.get(bill_id=bill_id)
            transaction.status = 3
            transaction.save()
            process_step += lifetime
        
        if status == 'ERROR':
            logger.info('if статус счета ' + status)
            transaction = Deposit.objects.get(bill_id=bill_id)
            transaction.status = 4
            transaction.save()
            process_step += lifetime

        time.sleep(60)
        

@shared_task
def post_withdrawal_alert(username, amount, link):
    """отправить email админу после вывода средств"""
    # Собрать контексты для html странички
    html_content = render_to_string('MainApp/mailing.html',
                                    {'username': username, 'link': link, 'amount': amount})
    # Собрать тело сообщения
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новом отклике',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMINS[0][1], ]
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем
    logger.info(f'Письмо отправлено {settings.ADMINS}')