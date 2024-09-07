from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer
from .tasks import send_confirmation_email
from .utils import generate_confirmation_token

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            uidb64, token = generate_confirmation_token(user)

            confirmation_url = request.build_absolute_uri(
                f'/api/confirm-email/{uidb64}/{token}/'
            )
            send_confirmation_email.delay(user.email, confirmation_url)

            return Response(
                {"message": "Registration successful. Please confirm your email."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email confirmed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid confirmation link."}, status=status.HTTP_400_BAD_REQUEST)
