# -*- coding:utf-8 -*-
"""
@Time : 2024/2/20 20:50 PM
@Author: weaimy
@Des: JWT鉴权
"""
from datetime import timedelta, datetime
import jwt
from jwt import PyJWTError
from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from manager.models import Admin

def create_access_token(data):
    """
    创建token
    :param data: 加密数据
    :return: jwt
    """
    token_data = data.copy()
    # token超时时间
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 向jwt加入超时时间
    token_data.update({"exp": expire})
    # jwt加密
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token


class MyBearerAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if request.get_full_path().startswith("/api/schema"):
            return (None, None)
        
        if authorization:
            scheme, _, param = authorization.partition(" ")

        if not authorization or scheme.lower() != "bearer":
            raise AuthenticationFailed({"code":401, "detail":"无效凭证"})
        
        token = param
        try:
            # token解密
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            if payload:
                # 用户对象
                user_id = payload.get("user_id", None)
                
                # 无效用户信息
                if user_id is None:
                    raise AuthenticationFailed({"code":401, "detail":"无效凭证"})
            else:
                credentials_exception = AuthenticationFailed({"code":401, "detail":"无效凭证"})
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"code":401, "detail":"无效凭证"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"code":401, "detail":"无效凭证"})
        except (PyJWTError):
            raise AuthenticationFailed({"code":401, "detail":"无效凭证"})
    
        # 查询用户是否真实有效、或者已经被禁用
        user_object = Admin.objects.get(pk=user_id)
        if user_object:
            return user_object, token
        raise AuthenticationFailed({"code":401, "detail":"无效凭证"})