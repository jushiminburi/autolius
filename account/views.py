from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .renderers import UserRenderer
from .serializers import (
    UserRegisterSerializer,
    LoginUserSerializer,
    UserProfileSerializer,
    ChangePasswordUserSerializer,
    SendNotifyPasswordByEmailUserSerializer,
    UserResetPasswordSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
                {"token": token, "message": "Register successful!"},
                status=status.HTTP_201_CREATED,
            )

class LoginUserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "message": "Login Successful"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Login Failed"}, status=status.HTTP_404_NOT_FOUND
                )



class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordUserView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordUserSerializer(data=request.data)
        serializer = ChangePasswordUserSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
                {"message": "Change Password Successful"},
                status=status.HTTP_200_OK,
            )



class SendNotifyPasswordByEmailUserView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendNotifyPasswordByEmailUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )


class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )
