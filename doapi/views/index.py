from typing import Any
from django.http import Http404
from django.contrib.auth.hashers import check_password
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

from manager.models import ContentModel, Admin as AdminModel
from doapi.serializers import LoginSerializers, ContentSerializers
from doapi.core.auth import create_access_token
from doapi.core.perm import UserPermission, ManagerPermission, BossPermission

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# 创建验证码
class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        hashkey = CaptchaStore.generate_key() # 验证码答案
        image_url = captcha_image_url(hashkey) # 验证码地址
        return Response({'hashkey': hashkey, 'image_url': image_url})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    @extend_schema(
        # parameters=[
        #     OpenApiParameter(name='adminname', description='Admin name', required=True, type=str),
        #     OpenApiParameter(name='adminpass', description='Admin password', required=True, type=str),
        # ],
        request = LoginSerializers,
        responses = Any,
        auth = None,
        # exclude = True,

    )
    def post(self, request):
        
        adminname = request.data.get('adminname')
        adminpass = request.data.get('adminpass')
        captcha = request.data.get("captcha", None)
        hashkey = request.data.get("captcha_0", None)

         # 用户名密码校验
        if not adminname or not adminpass:
            return Response({"code": 500, "msg": "登录信息错误"})
        else:
            admin_info = AdminModel.objects.filter(adminname=adminname).first()

            if not admin_info:
                return Response({"code": 500, "msg": "用户名不存在"})
            else:
                if check_password(adminpass, admin_info.adminpass):
                    
                    # if captcha:
                    #     if not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
                    #         return Response({"code": 500, "msg": "验证码信息错误"})
                    #     else:
                            jwt_data = {
                                "user_id": admin_info.adminid
                            }
                            jwt_token = create_access_token(data=jwt_data)
                            return Response({"code": 200, "msg": "登录成功", "token": jwt_token})
                    # return Response({"code": 500, "msg": "验证码不能为空"})
                else:
                    return Response({"code": 500, "msg": "用户密码不正确"})


class ContentViewSet(viewsets.ViewSet):
    def list(self, request):
        users = ContentModel.objects.all()
        serializer = ContentSerializers(users, many=True)
        return Response(serializer.data)

    # def create(self, request):
    #     serializer = ContentSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            user = ContentModel.objects.get(id=pk)
        except ContentModel.DoesNotExist:
            raise Http404

        serializer = ContentSerializers(user)
        return Response(serializer.data)

    def update(self, request, pk):
        try:
            user = ContentModel.objects.get(id=pk)
        except ContentModel.DoesNotExist:
            raise Http404

        serializer = ContentSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def destroy(self, request, pk):
    #     try:
    #         content = ContentModel.objects.get(id=pk)
    #     except ContentModel.DoesNotExist:
    #         raise Http404

    #     content.delete()
    #     return Response("")