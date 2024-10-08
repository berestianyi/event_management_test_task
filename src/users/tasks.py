import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_confirmation_email(email: str, confirmation_url: str):
    send_mail(
        subject='Email Confirmation',
        message=f'Please confirm your email by clicking the following link: {confirmation_url}',
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )
