from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token


from auth.serializers import LoginSerializer, RegisterSerializer


class AuthViewSet(ViewSet):

    @action(detail=False, methods=['post'] , permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            email = User.objects.get(email=email)
            if email.check_password(password):
                token, created = Token.objects.get_or_create(user=email)
                return Response({'token': token.key})
            return Response({'message': 'Username / Password is Invalid'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)



    @action(detail=False, methods=['post'] , permission_classes=[AllowAny])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        User.objects.create_user(username=username, password=password , email=email)

        return Response({'message': f'Hello {username}.'},status=status.HTTP_201_CREATED)



    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):

        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'], url_path='profile', permission_classes=[IsAuthenticated])
    def profile(self, request):
        return Response(
            {
                'username': request.user.username,
                'email': request.user.email,
            }
        )