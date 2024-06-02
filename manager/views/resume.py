from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ContentModel, CategoryModel, TagsModel, ModelJobModel, JobFormModel
from django.core.paginator import Paginator

import json 
import time


# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/resume/add.html", locals())

    def post(self, request):
        ip = get_client_ip(request)
        JobFormModel.objects.create(
            my_title = request.POST.get("my_title"),
            my_truename = request.POST.get("my_truename"),
            my_sex = request.POST.get("my_sex"),
            my_age = request.POST.get("my_age"),
            my_mobile = request.POST.get("my_mobile"),
            my_education = request.POST.get("my_education"),
            my_work_exp = request.POST.get("my_work_exp"),
            my_intro = request.POST.get("my_intro"),
            my_ip = ip,
            islock = request.POST.get("islock"),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request):
        id = request.GET.get('id')

        data_dict = {}
        content_info = JobFormModel.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/resume/edit.html", data_dict)

    def post(self, request):
        id = request.GET.get('id')
        ip = get_client_ip(request)
        JobFormModel.objects.filter(id=id).update(
            my_title = request.POST.get("my_title"),
            my_truename = request.POST.get("my_truename"),
            my_sex = request.POST.get("my_sex"),
            my_age = request.POST.get("my_age"),
            my_mobile = request.POST.get("my_mobile"),
            my_education = request.POST.get("my_education"),
            my_work_exp = request.POST.get("my_work_exp"),
            my_intro = request.POST.get("my_intro"),
            my_ip = ip,
            ordnum = request.POST.get("ordnum"),
            islock = request.POST.get("islock"),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    

# 添加内容
class IndexView(View):
    def get(self, request):
        try:
            content_items = JobFormModel.objects.order_by('-create_time').all()
        except JobFormModel.DoesNotExist:
            content_items=[]

        paginator = Paginator(content_items, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "manager/resume/index.html",locals())

    def post(self, request):
        # result = {"state": "success", "msg": "保存成功"}
        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)
    
def switchs(request):
    id = request.GET.get("id", 0)
    state = request.POST.get("state", 0)

    JobFormModel.objects.filter(id=id).update(islock=state)
    result = {"state": "success", "msg": "提交成功"}

    return JsonResponse(result, safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip