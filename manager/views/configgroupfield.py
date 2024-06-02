from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ConfigGroupModel, ConfigModel
from django.core.paginator import Paginator
import json

class IndexView(View):
    def get(self, request, gid):
        try:
            data_items = ConfigModel.objects.filter(gid=gid).order_by('ordnum', 'id')
        except ConfigModel.DoesNotExist:
            data_items = []

        return render(request,"manager/system/field/index.html", locals())

    def post(self, request, gid):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            ConfigModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class AddView(View):
    def get(self, request, gid):
        return render(request,"manager/system/field/add.html", locals())

    def post(self, request, gid):
        dvalue = request.POST.get('dvalue', 0)
        if dvalue:
            dvalue = dvalue.replace('\r\n', '\n').split('\n')
            dvalue = ','.join(dvalue)
        data = {
            'gid': gid,
            'ctitle': request.POST.get('ctitle'),
            'ckey': request.POST.get('ckey'),
            'ctype': request.POST.get('ctype', 0),
            'dvalue': dvalue,
            'utype': request.POST.get('utype', 0),
            'dtext': request.POST.get('dtext', 0),
            'rtype': request.POST.get('rtype', 0),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        ConfigModel.objects.create(**data)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class EditView(View):
    def get(self, request, id):
        book_info = ConfigModel.objects.get(id=id)
        if book_info.dvalue:
            book_info.dvalue = book_info.dvalue.replace(',', '\r\n')
        data_dict = book_info.__dict__

        return render(request,"manager/system/field/edit.html", data_dict)

    def post(self, request, id):
        dvalue = request.POST.get('dvalue', 0)
        if dvalue:
            dvalue = dvalue.replace('\r\n', '\n').split('\n')
            dvalue = ','.join(dvalue)
        print(dvalue)
        data = {
            'ctitle': request.POST.get('ctitle'),
            'ctype': request.POST.get('ctype', 0),
            'dvalue': dvalue,
            'utype': request.POST.get('utype', 0),
            'dtext': request.POST.get('dtext', 0),
            'rtype': request.POST.get('rtype', 0),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        ConfigModel.objects.filter(pk=id).update(**data)

        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


def switchs(request, id):
    islock = request.POST.get("islock", 0)
    ConfigModel.objects.filter(id=id).update(islock=islock)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def delete(request, id):
    info = ConfigModel.objects.get(pk=id)
    if info.issys:
        result = {"state": "error", "msg": "系统字段不能删除"}
        return JsonResponse(result, safe=False)
    ConfigModel.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)