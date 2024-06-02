from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import UserGroupModel
from django.core.paginator import Paginator

class IndexView(View):
    def get(self, request):
        try:
            usergroup_items = UserGroupModel.objects.order_by('ordnum').all()
        except UserGroupModel.DoesNotExist:
            usergroup_items=[]
        return render(request, "manager/user/group/index.html",locals())
    
    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            UserGroupModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 编辑会员组
class AddView(View):
    def get(self, request):
        return render(request, "manager/user/group/add.html", locals())

    def post(self, request):
        data = {
            "gname" : request.POST.get("gname"),
            "ordnum" : request.POST.get("ordnum", 0),
        }
        obj = UserGroupModel.objects.create(**data)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

# 编辑会员组
class EditView(View):
    def get(self, request, id):
        info = UserGroupModel.objects.get(gid=id)
        data_dict = info.__dict__
        return render(request, "manager/user/group/edit.html", data_dict)

    def post(self, request, id):
        data = {
            "gname" : request.POST.get("gname"),
            "ordnum" : request.POST.get("ordnum", 0),
        }
        obj = UserGroupModel.objects.filter(gid=id).update(**data)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    

def delete(request, id):
    UserGroupModel.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)