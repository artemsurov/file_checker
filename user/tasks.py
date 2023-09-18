import logging

from django.core.mail import send_mail

from conf import celery_app

file_checker = logging.getLogger('file_checker')


@celery_app.task()
def notify_user(user_email, file_name, results):
    send_mail(
        'Your file has been validated',
        f'Your file {file_name} has been validated with results: {results}',
        from_email=None,
        recipient_list=[user_email],
        fail_silently=True,
        )
    file_checker.info('Email has been sent to %s with results: %s', user_email, results)
