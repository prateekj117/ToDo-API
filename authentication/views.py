from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from authentication.renderers import UserRenderer
from authentication.serializers import UserRegistrationSerializer

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
