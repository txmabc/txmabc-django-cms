from doapi import views
from rest_framework import routers
from doapi.views import index
from django.urls import path,include

app_name="doapi"

router = routers.DefaultRouter()
router.register('content', index.ContentViewSet, basename='content')

urlpatterns = [
    path('captcha/', index.CaptchaView.as_view(), name='captcha'),
    path('login/', index.LoginView.as_view(), name='login'),
]
urlpatterns += router.urls