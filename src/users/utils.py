from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import User


def generate_confirmation_token(user: User) -> tuple:
    return urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)
