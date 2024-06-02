from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import BookModel
from django.core.paginator import Paginator

class IndexView(View):
    def get(self, request):
        type = 0
        keyword = ''
        try:
            content_items = BookModel.objects.order_by('-create_time').all()
        except BookModel.DoesNotExist:
            content_items=[]

        paginator = Paginator(content_items, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "manager/extend/book/index.html",locals())


# 编辑内容
class EditView(View):
    def get(self, request, id):
        book_info = BookModel.objects.get(id=id)
        data_dict = book_info.__dict__
        return render(request, "manager/extend/book/edit.html", data_dict)

    def post(self, request, id):
        data = {
            "truename" : request.POST.get("truename"),
            "tel" : request.POST.get("tel"),
            "mobile" : request.POST.get("mobile"),
            "remark" : request.POST.get("remark"),
            "reply" : request.POST.get("reply"),
            "ontop" : request.POST.get("ontop", 0),
            "islock" : request.POST.get("islock", 1),
        }
        obj = BookModel.objects.filter(id=id).update(**data)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    
def switchs(request):
    id = request.GET.get("id", 0)
    type = request.GET.get("type", 0)
    state = request.POST.get("state", 0)
    if type == '1':
        BookModel.objects.filter(id=id).update(ontop=state)
        result = {"state": "success", "msg": "提交成功"}
    if type == '2':
        BookModel.objects.filter(id=id).update(islock=state)
        result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def delete(request):
    BookModel.objects.filter(pk=request.GET.get("id")).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)