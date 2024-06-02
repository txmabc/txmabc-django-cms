from django.shortcuts import render
from django.http import JsonResponse
from manager.models import TagsModel
from django.core.paginator import Paginator

# 添加内容
def index(request):
    try:
        if request.GET.get('keyword'):
            keyword=request.GET.get('keyword').strip()
            content_items = TagsModel.objects.get(title__contains=keyword)
        else:
            content_items = TagsModel.objects.all()
    except TagsModel.DoesNotExist:
        content_items=[]

    paginator = Paginator(content_items, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "manager/extend/tags.html",locals())


def clear(request):
    TagsModel.objects.filter(hits=0).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)    


def delete(request, id):
    TagsModel.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)