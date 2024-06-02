from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import Admin, AdminPart
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password, make_password
import json


class IndexView(View):
    def get(self, request):
        try:
            admin_items = Admin.objects.order_by('adminid').all()
        except Admin.DoesNotExist:
            admin_items=[]
        
        if admin_items:
            for i in range(0,len(admin_items)):
                if admin_items[i].pid:
                    admin_items[i].title = AdminPart.objects.get(pk = admin_items[i].pid).title
        return render(request,"manager/config/admin/index.html", locals())


class AddView(View):
    def get(self, request):
        return render(request,"manager/config/admin/add.html", locals())

    def post(self, request):
        data = {
            'adminname': request.POST.get('adminname'),
            'adminpass': make_password(request.POST.get('adminpass')),
            'penname': request.POST.get('penname'),
            'pid': request.POST.get('pid'),
            'islock': request.POST.get('islock'),
            'readonly': request.POST.get('readonly'),
        }
        Admin.objects.create(**data)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = Admin.objects.get(adminid=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request,"manager/config/admin/edit.html", data_dict)

    def post(self, request, id):
        data = {
            'penname': request.POST.get('penname'),
            'pid': request.POST.get('pid'),
            'islock': request.POST.get('islock'),
            'readonly': request.POST.get('readonly'),
        }
        adminpass = request.POST.get('adminpass').strip()
        if adminpass:
             data.update({
                'adminpass': make_password(request.POST.get('adminpass')),
            })
        Admin.objects.filter(pk=id).update(**data)

        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


def delete(request, id):
	if id == request.session.get("adminid"):
		result = {"state": "fail", "msg": "不能删除自己"}
	else:
		Admin.objects.filter(pk=id).delete()
		result = {"state": "success", "msg": "删除成功"}
	return JsonResponse(result, safe=False)


def switchs(request, type, id):
    state = request.POST.get("state", 0)
    if type == 1:
        Admin.objects.filter(pk=id).update(islock=state)
    if type == 2:
        Admin.objects.filter(pk=id).update(readonly=state)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)