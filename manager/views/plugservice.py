from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import PlugService

# 添加内容
class IndexView(View):
    def get(self, request):
        try:
            plugservice_items = PlugService.objects.order_by('ordnum').all()
        except PlugService.DoesNotExist:
            plugservice_items=[]

        return render(request, "manager/plug/service/index.html",locals())

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            PlugService.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/plug/service/add.html", locals())

    def post(self, request):
        PlugService.objects.create(
            title = request.POST.get("title"),
            qq = request.POST.get("qq"),
            ordnum = request.POST.get("ordnum", 0),
            islock = request.POST.get("islock", 0),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = PlugService.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/plug/service/edit.html", data_dict)

    def post(self, request, id):
        PlugService.objects.filter(id=id).update(
            title = request.POST.get("title"),
            qq = request.POST.get("qq"),
            ordnum = request.POST.get("ordnum", 0),
            islock = request.POST.get("islock", 0),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
        
def delete(request, id):
    PlugService.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)