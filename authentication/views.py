from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate

from authentication.renderers import UserRenderer
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer

def get_tokens_for_user(user):
    """
    Generate refresh and access tokens
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(GenericAPIView):
    """
    View for user registration
    """
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer
    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'msg': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def post(self, request):
        """
        Method to run on user registration post request
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                { 'token' : token, 'msg' : 'Registration Success'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(GenericAPIView):
    """
    View for user login
    """
    renderer_classes = [UserRenderer]
    serializer_class = UserLoginSerializer
    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'msg': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def post(self, request):
        """
        Method to run on user login post request
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    { 'token' : token, 'msg' : 'Login Success' },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'errors': {
                        'non_field_errors' : ['Email or Password is not Valid']
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
