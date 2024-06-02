from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import UserModel, UserGroupModel
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q

import json 
import time

# 列表内容
class IndexView(View):
    def get(self, request, uid=0, type=0):
        keyword = ''
        try:
            if uid:
                content_items = UserModel.objects.filter(uid=uid).order_by('-regdate').all()
            elif type == 1:
                content_items = UserModel.objects.filter(islock=1).order_by('-regdate').all()
            elif type == 2:
                content_items = UserModel.objects.filter(islock=0).order_by('-regdate').all()
            elif type == 3:
                content_items = UserModel.objects.filter(uface__isnull=False).order_by('-regdate').all()
            else:
            
                content_items = UserModel.objects.order_by('-regdate').all()
        except UserModel.DoesNotExist:
            content_items=[]
        
        for i in range(0, len(content_items)):
            
            content_items[i].gname=UserGroupModel.objects.get(pk=content_items[i].uid).gname

        paginator = Paginator(content_items, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        groupitems = UserGroupModel.objects.order_by('ordnum').all()

        return render(request, "manager/user/index.html",locals())

    def post(self, request):
        result = {"state": "fail", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 添加会员
class AddView(View):
    def get(self, request):
        groupitems = UserGroupModel.objects.order_by('ordnum').all()
        return render(request, "manager/user/add.html",locals())

    def post(self, request):
        username = request.POST.get('uname')
        upass = request.POST.get('upass')
        if UserModel.objects.filter(uname=username).exists():
            result = {"state": "fail", "msg": "用户名已存在"}
            return JsonResponse(result, safe=False)
        else:
            data = {
                'uname': username,
                'upass': make_password(upass),
                'uemail': request.POST.get('uemail'),
                'uid': request.POST.get('uid'),
                'islock': request.POST.get('islock'),
            }
        
            UserModel.objects.create(**data)
            result = {"state": "success", "msg": "保存成功"}
            return JsonResponse(result, safe=False)
    

# 编辑会员
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = UserModel.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        groupitems = UserGroupModel.objects.order_by('ordnum').all()

        data_dict.update({'groupitems':groupitems})

        return render(request, "manager/user/edit.html",data_dict)

    def post(self, request, id):
        data = {
            'uname': request.POST.get('uname'),
            'uemail': request.POST.get('uemail'),
            'uid': request.POST.get('uid'),
            'islock': request.POST.get('islock'),
        }
        upass = request.POST.get('upass')
        if upass:
            data.update({'upass': make_password(upass)})

        UserModel.objects.filter(pk=id).update(**data)
        result = {"state": "fail", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    

def switchs(request, id):
    state = request.POST.get("state")
    UserModel.objects.filter(id=id).update(islock=state)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def gouser(request, id):
    username = UserModel.objects.get(pk=id).uname
    request.session["username"] = username
    return redirect(reverse('users:index'))


def clear(request, id):
    UserModel.objects.filter(pk=id).update(uface='')
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def delete(request, id):
    UserModel.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)