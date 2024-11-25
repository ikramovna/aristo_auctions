import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from root import settings
from src.users.models import User, getKey
from src.users.serializers import (UserRegisterSerializer, CheckActivationCodeSerializer, ResetPasswordSerializer,
                                   ResetPasswordConfirmSerializer, UserSerializer, UserModelSerializer)


class UserRegisterCreateAPIView(CreateAPIView):
    """
    API endpoint that allows users to be registered.

    Example request:
    """
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckActivationCodeGenericAPIView(GenericAPIView):
    """
    API endpoint that allows users to be checked activation code.

    Example request:
    """
    serializer_class = CheckActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = getKey(key=data['email'])['user']
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Your email has been confirmed",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


class ResetPasswordView(CreateAPIView):
    """
    API endpoint that allows users to be reset password.

    Example request:
    """
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            activation_code = str(random.randint(100000, 999999))

            # Set new password
            user.set_password(activation_code)
            user.save()

            # Send email with activation code
            subject = "Password Reset Confirmation"
            html_content = render_to_string('forget_password.html', {'activation_code': activation_code})
            text_content = strip_tags(html_content)

            from_email = f"Aura Team <{settings.EMAIL_HOST_USER}>"
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"detail": "Password reset code sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(CreateAPIView):
    """
    API endpoint that allows users to be reset password confirm.

    Example request:
    """
    serializer_class = ResetPasswordConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(activation_code):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "New password and confirm password do not match."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Invalid activation code."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be updated.

    Example request:
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'put']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user


class UserCreateAPIView(CreateAPIView):
    """
    API endpoint that allows users to be created.

    Example request:
    """
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
