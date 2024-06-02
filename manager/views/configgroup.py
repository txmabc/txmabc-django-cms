from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ConfigGroupModel, ConfigModel
from django.core.paginator import Paginator
import json

class IndexView(View):
    def get(self, request):
        try:
            data_items = ConfigGroupModel.objects.filter(gkey=0).order_by('ordnum', 'id')
        except ConfigGroupModel.DoesNotExist:
            data_items = []

        return render(request,"manager/system/group/index.html", locals())

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            ConfigGroupModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class AddView(View):
    def get(self, request):
        return render(request,"manager/system/group/add.html", locals())

    def post(self, request):
        data = {
            'gname': request.POST.get('gname'),
            'gkey': request.POST.get('gkey', '0'),
            'ordnum': request.POST.get('ordnum', 0),
            'types': request.POST.get('types', 0),
            'islock': request.POST.get('islock', 0),
        }
        ConfigGroupModel.objects.create(**data)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class EditView(View):
    def get(self, request, id):
        book_info = ConfigGroupModel.objects.get(id=id)
        data_dict = book_info.__dict__

        return render(request,"manager/system/group/edit.html", data_dict)

    def post(self, request, id):
        data = {
            'gname': request.POST.get('gname'),
            'ordnum': request.POST.get('ordnum', 0),
            'types': request.POST.get('types', 0),
            'islock': request.POST.get('islock', 0),
        }
        ConfigGroupModel.objects.filter(pk=id).update(**data)

        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


def switchs(request, id):
    islock = request.POST.get("islock", 0)
    ConfigGroupModel.objects.filter(id=id).update(islock=islock)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def delete(request, id):
    count = ConfigModel.objects.filter(gid=id).count()
    print(count)
    if count:
        result = {"state": "fail", "msg": "请先删除分组的字段"}
    # ConfigGroupModel.objects.filter(pk=id).delete()
    # result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)