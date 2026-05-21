from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AuthViewSet, CompanyViewSet, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
