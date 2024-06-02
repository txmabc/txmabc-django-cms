from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import Order
import urllib.parse

# 添加内容
def index(request):
    type = int(request.GET.get("type", 0))
    where = '1=1 '
    keyword = ''
    if request.GET.get("keyword"):
        keyword= urllib.parse.unquote(request.GET.get("keyword"))

    return render(request, "manager/extend/order/index.html",locals())


# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = Order.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/extend/order/edit.html", data_dict)

    def post(self, request, id):
        Order.objects.filter(id=id).update(
            truename = request.POST.get("truename"),
            mobile = request.POST.get("mobile"),
            address = request.POST.get("address"),
            remark = request.POST.get("remark"),
            isover = request.POST.get("islock", 0),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
        
def delete(request, id):
    Order.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)


def btach(request):
    type = int(request.POST.get("type", 0))
    id = request.POST.get("id")
    if type == 1:
        btach_some("isover", 1, id)
    if type == 2:
        btach_some("isover", 0, id)
    result = {"state": "fail", "msg": "操作失败"}
    return JsonResponse(result, safe=False)

def btach_some(field,val,id):
    d={}
    d[field]=val
    arr=id.split(',')
    for item in arr:
        item=int(item)
        Order.objects.filter(id=item).update(**d)

def btach_del(id):
    arr=id.split(',')
    for item in arr:
        item=int(item)
        Order.objects.filter(id=item).delete()


def switchs(request):
    id = int(request.GET.get("id", 0))
    state = int(request.POST.get("state", 0))
    Order.objects.filter(id=id).update(isover=state)

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)