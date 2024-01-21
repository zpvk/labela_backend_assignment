from rest_framework import generics
from django.contrib.auth.models import User
from api.serializers.userSerializer import UserSerializer
from api.serializers.tokenResponseSerializer import TokenResponseSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
        
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer_class.Meta.model.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        serializer = TokenResponseSerializer({'token': token.key})
        return Response(serializer.data, status=200)