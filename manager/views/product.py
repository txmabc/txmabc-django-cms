from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ContentModel, CategoryModel, TagsModel, ModelProModel

import json 
import time


# 添加内容
class AddView(View):
    def get(self, request):
        classid = request.GET.get("classid")
        return render(request, "manager/content/pro/add.html",locals())

    def post(self, request):
        classid = request.GET.get("classid")
        timeArray = time.strptime(request.POST.get("createdate"), "%Y-%m-%d %H:%M:%S")
        createdate = int(time.mktime(timeArray))
        ispic = 1 if request.POST.get("pic") else 0

        data = {
            "classid": classid,
            "title" : request.POST.get("title"),
            "pic" : request.POST.get("pic"),
            "ispic" : ispic,
            "tags" : request.POST.get("tags"),
            "intro" : request.POST.get("intro"),
            "seotitle" : request.POST.get("seotitle"),
            "seokey" : request.POST.get("seokey"),
            "seodesc" : request.POST.get("seodesc"),
            "alias" : request.POST.get("alias"),
            "url" : request.POST.get("url"),
            "upnum" : request.POST.get("upnum"),
            "downnum" : request.POST.get("downnum"),
            "ordnum" : request.POST.get("ordnum"),
            "ontop" : request.POST.get("ontop"),
            "isnice" : request.POST.get("isnice"),
            "isauto" : request.POST.get("isauto"),
            "showskin" : request.POST.get("showskin"),
            "createdate" : createdate,
        }

        obj = ContentModel.objects.create(**data)

        ndata = {
            "cid" : obj.id,
            "content" : request.POST.get("content"),
            "price" : request.POST.get("price"),
            "piclist" : request.POST.get("piclist"),
        }

        nobj = ModelProModel.objects.create(**ndata)

        result = {"state": "success", "msg": "保存成功"}
        # result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request):
        classid = request.GET.get('classid')
        id = request.GET.get('id')

        data_dict = {}
        content_info = ContentModel.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        content_extend_info = ModelProModel.objects.get(cid = id)
        content_extend_dict = content_extend_info.__dict__
        data_dict.update(content_extend_dict)
        if content_extend_dict['piclist']:
            picdata = json.loads(content_extend_dict['piclist'])
            data_dict.update({'picdata': picdata})
        
        return render(request, "manager/content/pro/edit.html", data_dict)


    def post(self, request):
        classid = request.GET.get("classid")
        id = request.GET.get("id")
        # result = {"state": "fail", "msg": "保存失败"}
        # return JsonResponse(result, safe=False)
        
        timeArray = time.strptime(request.POST.get("createdate"), "%Y-%m-%d %H:%M:%S")
        createdate = int(time.mktime(timeArray))

        ispic = 1 if request.POST.get("pic") else 0

        data = {
            "classid": classid,
            "title" : request.POST.get("title"),
            "pic" : request.POST.get("pic"),
            "ispic" : ispic,
            "tags" : request.POST.get("tags"),
            "intro" : request.POST.get("intro"),
            "seotitle" : request.POST.get("seotitle"),
            "seokey" : request.POST.get("seokey"),
            "seodesc" : request.POST.get("seodesc"),
            "alias" : request.POST.get("alias"),
            "url" : request.POST.get("url"),
            "upnum" : request.POST.get("upnum"),
            "downnum" : request.POST.get("downnum"),
            "ordnum" : request.POST.get("ordnum"),
            "ontop" : request.POST.get("ontop"),
            "isnice" : request.POST.get("isnice"),
            "isauto" : request.POST.get("isauto"),
            "showskin" : request.POST.get("showskin"),
            "createdate" : createdate,
        }

        obj = ContentModel.objects.filter(id=id).update(**data)

        ndata = {
            "content" : request.POST.get("content"),
            "price" : request.POST.get("price"),
            "piclist" : request.POST.get("piclist"),
        }

        nobj = ModelProModel.objects.filter(cid=id).update(**ndata)

        result = {"state": "success", "msg": "保存成功"}
        # result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)