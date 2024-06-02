from django.shortcuts import render
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views import View
from manager.models import Admin
