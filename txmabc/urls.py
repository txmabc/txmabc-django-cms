"""
URL configuration for txmabc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static

from . import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
	path("", include("home.urls")),
    path("manager/", include("manager.urls")),
	path("users/", include("users.urls")),
	path("api/", include("doapi.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('captcha/', include('captcha.urls')),  
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger接口文档
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc接口文档
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
