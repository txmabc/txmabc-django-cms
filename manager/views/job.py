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
        classid = request.GET.get("classid")
        return render(request, "manager/content/job/add.html",locals())

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
            "work_address" : request.POST.get("work_address"),
            "work_nature" : request.POST.get("work_nature"),
            "work_education" : request.POST.get("work_education"),
            "work_money" : request.POST.get("work_money"),
            "work_age" : request.POST.get("work_age"),
            "work_num" : request.POST.get("work_num"),
        }

        nobj = ModelJobModel.objects.create(**ndata)

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

        # print(content_dict)

        content_extend_info = ModelJobModel.objects.get(cid = id)
        content_extend_dict = content_extend_info.__dict__
        data_dict.update(content_extend_dict)
        # print(content_extend_dict)

        return render(request, "manager/content/job/edit.html", data_dict)

    def post(self, request):
        classid = request.GET.get("classid")
        id = request.GET.get("id")

        timeArray = time.strptime(request.POST.get("createdate"), "%Y-%m-%d %H:%M:%S")
        createdate = int(time.mktime(timeArray))

        tags = request.POST.get("tags")
        tagslist = []

        if tags:
            if ',' in tags:
                tagarr = tags.split(',')
                for tag in tagarr:
                    try:
                        taginfo = TagsModel.objects.filter(title=tag).get()
                        tagslist.append({'name':taginfo.title, 'id':taginfo.id})
                    except TagsModel.DoesNotExist:
                        taginfo = TagsModel.objects.create(title=tag)
                        tagslist.append({'name':taginfo.title, 'id':taginfo.id})
            else:
                try:
                    taginfo = TagsModel.objects.filter(title=tags).get()
                    tagslist.append({'name':taginfo.title, 'id':taginfo.id})
                except TagsModel.DoesNotExist:
                    taginfo = TagsModel.objects.create(title=tags)
                    tagslist.append({'name':taginfo.title, 'id':taginfo.id})

        ispic = 1 if request.POST.get("pic") else 0

        data = {
            "classid": classid,
            "title" : request.POST.get("title"),
            "pic" : request.POST.get("pic"),
            "ispic" : ispic,
            "tags" : request.POST.get("tags"),
            "tagslist": tagslist,
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
            "work_address" : request.POST.get("work_address"),
            "work_nature" : request.POST.get("work_nature"),
            "work_education" : request.POST.get("work_education"),
            "work_money" : request.POST.get("work_money"),
            "work_age" : request.POST.get("work_age"),
            "work_num" : request.POST.get("work_num"),
        }

        nobj = ModelJobModel.objects.filter(cid=id).update(**ndata)

        result = {"state": "success", "msg": "保存成功"}
        # result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)