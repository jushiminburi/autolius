
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .serializers import UserRegisterSerializer
from django.http import JsonResponse


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            
            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)