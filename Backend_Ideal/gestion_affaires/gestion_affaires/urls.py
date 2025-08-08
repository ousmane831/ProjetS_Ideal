"""
URL configuration for gestion_affaires project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django & Django REST Framework Imports
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Swagger / Redoc Documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# JWT Authentication
from Affaires.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

# Schema View Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="API de gestion des affaires",
        default_version='v1',
        description="Documentation de l'API",
        contact=openapi.Contact(email="contact@exemple.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URL Patterns
urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # App Routes
    path('api/', include('Affaires.urls')),

    # JWT Authentication Endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger and Redoc Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
