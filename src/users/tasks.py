import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_confirmation_email(email: str, confirmation_url: str):
    subject = 'Email Confirmation'
    message = f'Please confirm your email by clicking the following link: {confirmation_url}'
    send_mail(
        subject,
        message,
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )
