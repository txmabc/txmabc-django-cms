from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import AdvertModel
from django.core.paginator import Paginator
import json

class IndexView(View):
    def get(self, request):
        try:
            advert_items = AdvertModel.objects.order_by('ordnum')
        except AdvertModel.DoesNotExist:
            advert_items=[]
        return render(request,"manager/extend/ad/index.html", locals())

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            AdvertModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class AddView(View):
    def get(self, request):
        return render(request,"manager/extend/ad/add.html", locals())

    def post(self, request):
        data = {
            'title': request.POST.get('title'),
            'datalist': request.POST.get('datalist'),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        AdvertModel.objects.create(**data)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class EditView(View):
    def get(self, request, id):
        book_info = AdvertModel.objects.get(id=id)
        data_dict = book_info.__dict__
        if data_dict['datalist']:
            picdata = json.loads(data_dict['datalist'])
            data_dict.update({'picdata': picdata})

        return render(request,"manager/extend/ad/edit.html", data_dict)

    def post(self, request, id):
        data = {
            'title': request.POST.get('title'),
            'datalist': request.POST.get('datalist'),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        AdvertModel.objects.filter(pk=id).update(**data)

        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


def switchs(request):
    id = request.GET.get("id", 0)
    islock = request.POST.get("islock", 0)
    AdvertModel.objects.filter(id=id).update(islock=islock)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)