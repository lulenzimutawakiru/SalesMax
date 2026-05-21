from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Company
from .serializers import (
    UserSerializer, RegisterSerializer, CompanySerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with additional user information."""
    serializer_class = CustomTokenObtainPairSerializer


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints."""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Incorrect password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user information."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update user profile."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ModelViewSet):
    """Company management endpoints."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter companies based on user."""
        if self.request.user.role == 'admin':
            return Company.objects.all()
        return Company.objects.filter(id=self.request.user.company_id)
