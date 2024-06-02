from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ContentModel, CategoryModel, TagsModel, ModelNewsModel

import json 
import time


# 添加内容
class AddView(View):
    def get(self, request):
        classid = request.GET.get("classid")
        return render(request, "manager/content/news/add.html",locals())

    def post(self, request):
        classid = request.GET.get("classid")

        timeArray = time.strptime(request.POST.get("createdate"), "%Y-%m-%d %H:%M:%S")
        createdate = int(time.mktime(timeArray))

        ispic = 1 if request.POST.get("pic") else 0

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
            "upnum" : request.POST.get("upnum",0),
            "downnum" : request.POST.get("downnum",0),
            "ordnum" : request.POST.get("ordnum",0),
            "ontop" : request.POST.get("ontop",0),
            "islock" : request.POST.get("islock",0),
            "isnice" : request.POST.get("isnice",1),
            "isauto" : request.POST.get("isauto",1),
            "showskin" : request.POST.get("showskin"),
            "createdate" : createdate,
        }

        obj = ContentModel.objects.create(**data)

        ndata = {
            "cid" : obj.id,
            # "myfree" : request.POST.get("myfree"),
            "content" : request.POST.get("content"),
            "price" : request.POST.get("price"),
        }

        nobj = ModelNewsModel.objects.create(**ndata)

        for item in tagslist:
            tag = TagsModel.objects.get(title=item['name'])
            tag.hits += 1
            tag.save(update_fields=['hits'])

        result = {"state": "success", "msg": "保存成功"}
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

        content_extend_info = ModelNewsModel.objects.get(cid = id)
        content_extend_dict = content_extend_info.__dict__
        data_dict.update(content_extend_dict)
        # print(content_extend_dict)

        return render(request, "manager/content/news/edit.html", data_dict)

    def post(self, request):
        classid = request.GET.get("classid")
        id = request.GET.get("id")
        
        timeArray = time.strptime(request.POST.get("createdate"), "%Y-%m-%d %H:%M:%S")
        createdate = int(time.mktime(timeArray))
        view_lever = request.POST.getlist("view_lever[]")
        view_lever = ",".join(view_lever)

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
            "ispic": ispic,
            "tags" : request.POST.get("tags"),
            "tagslist": tagslist,
            "intro" : request.POST.get("intro"),
            "seotitle" : request.POST.get("seotitle"),
            "seokey" : request.POST.get("seokey"),
            "seodesc" : request.POST.get("seodesc"),
            "alias" : request.POST.get("alias"),
            "url" : request.POST.get("url"),
            "upnum" : request.POST.get("upnum",0),
            "downnum" : request.POST.get("downnum",0),
            "ordnum" : request.POST.get("ordnum",0),
            "ontop" : request.POST.get("ontop",0),
            "islock" : request.POST.get("islock",0),
            "isnice" : request.POST.get("isnice",1),
            "isauto" : request.POST.get("isauto",1),
            "showskin" : request.POST.get("showskin"),
            "createdate" : createdate,
            "view_groupid" : view_lever,
        }

        old_tagslist = ContentModel.objects.get(pk=id).tagslist
        obj = ContentModel.objects.filter(id=id).update(**data)

        ndata = {
            "content" : request.POST.get("content"),
            "price" : request.POST.get("price"),
        }

        nobj = ModelNewsModel.objects.filter(cid=id).update(**ndata)

        if old_tagslist:
            old_tagslist = json.loads(old_tagslist.replace("'", '"'))
            for item in old_tagslist:
                try:
                    tag = TagsModel.objects.get(title=item['name'])
                    if tag.hits>0:
                        tag.hits -= 1
                        tag.save(update_fields=['hits'])
                except TagsModel.DoesNotExist:
                    pass

        for item in tagslist:
            tag = TagsModel.objects.get(title=item['name'])
            tag.hits += 1
            tag.save(update_fields=['hits'])

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)