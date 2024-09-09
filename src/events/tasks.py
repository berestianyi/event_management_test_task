import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_registration_email(email, event_title):
    send_mail(
        subject=f"Registration Confirmation for {event_title}",
        message=f"Thank you for registering for {event_title}! We look forward to your participation.",
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )
