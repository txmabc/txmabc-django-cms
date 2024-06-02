from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views import View
from manager.models import Inquiry


def index(request):
    types = int(request.GET.get("type", 0))
    where='1=1 '
    keyword=request.GET.get("keyword")
    if keyword:
        where += " and (truename like '%" + keyword + "%' or mobile like '%" + keyword + "%')"
    if types == 1:
        where += ' and isover=0'
    if types == 2:
        where += ' and isover=1'

    return render(request, "manager/extend/inquiry/index.html",locals())

# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        return render(request, "manager/extend/inquiry/edit.html", data_dict)

    def post(self, request, id):
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


def btach(request):
    type = int(request.POST.get("type", 0))
    id = request.POST.get("id")
    if type == 1:
        btach_some("isover", 1, id)
    if type == 2:
        btach_some("isover", 0, id)
    if type == 3:
        btach_del(id)
    result = {"state": "success", "msg": "操作成功"}
    return JsonResponse(result, safe=False)


def btach_some(field,val,id):
    d={}
    d[field]=val
    arr=id.split(',')
    for item in arr:
        item=int(item)
        Inquiry.objects.filter(id=item).update(**d)

def btach_del(id):
    arr=id.split(',')
    for item in arr:
        item=int(item)
        Inquiry.objects.filter(id=item).delete()

def delete(request, id):
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)


def switchs(request):
    id = int(request.GET.get("id", 0))
    state = int(request.POST.get("state", 0))
    Inquiry.objects.filter(id=id).update(isover=state)

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)