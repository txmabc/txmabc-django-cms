from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import AdminMenu
from django.core.paginator import Paginator

import json 
import time

# 添加内容
class IndexView(View):
    def get(self, request, fid=0):
        try:
            menu_items = AdminMenu.objects.filter(followid=fid).order_by('ordnum').all()
        except AdminMenu.DoesNotExist:
            menu_items=[]

        return render(request, "manager/system/menu/index.html",locals())

    def post(self, request, fid=0):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            AdminMenu.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

# 添加内容
class AddView(View):
    def get(self, request, fid):
        return render(request, "manager/system/menu/add.html", locals())

    def post(self, request, fid):
        AdminMenu.objects.create(
            title = request.POST.get("title"),
            cname = request.POST.get("cname", ""),
            aname = request.POST.get("aname", ""),
            dname = request.POST.get("dname", ""),
            followid = fid,
            ordnum = request.POST.get("ordnum", 0),
            islock = request.POST.get("islock", 1),
        )
        result = {"state": "success", "msg": "保存成功"}
        # result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = AdminMenu.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/system/menu/edit.html", data_dict)

    def post(self, request, id):
        AdminMenu.objects.filter(id=id).update(
            title = request.POST.get("title"),
            cname = request.POST.get("cname", ""),
            aname = request.POST.get("aname", ""),
            dname = request.POST.get("dname", ""),
            followid = request.POST.get("followid", 0),
            ordnum = request.POST.get("ordnum", 0),
            islock = request.POST.get("islock", 1),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

def switchs(request, id):
    islock = request.POST.get("islock", 0)
    AdminMenu.objects.filter(id=id).update(islock=islock)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)
   
def delete(request, id):
    AdminMenu.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)