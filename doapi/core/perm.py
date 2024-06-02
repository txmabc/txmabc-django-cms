from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class MyIsAuthentication(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and not request.user.readonly)


class UserPermission(BasePermission):
    message = {'status': 405, 'message': '此接口需要会员权限'}
    def has_permission(self, request, view):
        print(self.message)
        return False


class ManagerPermission(permissions.BasePermission):
    message = {'status': 405, 'message': '此接口需要管理员权限'}
    def has_permission(self, request, view):
        print(self.message)
        return False


class BossPermission(BasePermission):
    message = {'status': 405, 'message': '此接口需要超级管理员权限'}
    def has_permission(self, request, view):
        print(self.message)
        return False