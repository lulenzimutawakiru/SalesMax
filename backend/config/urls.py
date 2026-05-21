from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to SaleMax API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'crm': '/api/crm/',
            'sales': '/api/sales/',
            'inventory': '/api/inventory/',
            'accounting': '/api/accounting/',
            'hr': '/api/hr/',
            'projects': '/api/projects/',
            'analytics': '/api/analytics/',
        }
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health & Root
    path('api/health/', health_check, name='health_check'),
    path('api/', api_root, name='api_root'),
    
    # App URLs
    path('api/auth/', include('apps.authentication.urls')),
    path('api/crm/', include('apps.crm.urls')),
    path('api/sales/', include('apps.sales.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/accounting/', include('apps.accounting.urls')),
    path('api/hr/', include('apps.hr.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
