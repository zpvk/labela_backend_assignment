from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from api.serializers.tokenResponseSerializer import TokenResponseSerializer
from api.serializers.errorSerializer import ErrorResponseSerializer
from rest_framework import status


class CustomAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            serializer = TokenResponseSerializer({'token': token.key})
            return Response(serializer.data, status=200)
        
        else:
            # Use the custom serializer to format the error response
            error_serializer = ErrorResponseSerializer(data={
                'errors': [
                    {'title': 'Invalid Credentials', 'detail': 'Unable to log in with provided credentials.'}
                ]
            })
            if not error_serializer.is_valid():
                print(error_serializer.errors)

            return Response(error_serializer.data, status=status.HTTP_401_UNAUTHORIZED)