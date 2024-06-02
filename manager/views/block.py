from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import BlockModel

def index(request):
    try:
        block_items = BlockModel.objects.order_by('id').all()
    except BlockModel.DoesNotExist:
        block_items=[]
    return render(request, 'manager/content/block/list.html', locals())


# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/content/block/add.html",locals())

    def post(self, request):
        data = {
            "title" : request.POST.get("title"),
            "key" : request.POST.get("key"),
            "content" : request.POST.get("content"),
        }
        obj = BlockModel.objects.create(**data)
        # result = {"state": "success", "msg": "保存成功"}
        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request):
        id = request.GET.get('id')
        block_info = BlockModel.objects.get(id=id)
        data_dict = block_info.__dict__
        return render(request, "manager/content/block/edit.html", data_dict)

    def post(self, request):
        id = request.GET.get("id")
        data = {
            "title" : request.POST.get("title"),
            "key" : request.POST.get("key"),
            "content" : request.POST.get("content"),
        }

        obj = BlockModel.objects.filter(id=id).update(**data)

        result = {"state": "success", "msg": "保存成功"}
        # result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)
    
def delete(request, id):
    BlockModel.objects.filter(pk=id).delete()

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)