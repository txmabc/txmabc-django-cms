from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ContentModel, CategoryModel, ModelPageModel, TagsModel
from django.core.paginator import Paginator

import json 
import time


class IndexView(View):
    def get(self, request):
        zNodes = gen_zNodes(0,[])
        return render(
            request,
            "manager/content/index.html",
            locals()
        )

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            ContentModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 编辑栏目
class PageView(View):
    def get(self, request):
        classid = request.GET.get("classid")
        try:
            pageinfo = ModelPageModel.objects.get(cid=classid)
            data_dict = pageinfo.__dict__
            picdata = json.loads(data_dict['piclist'])
            data_dict.update({'picdata': picdata})
            # print(data_dict)
        except ModelPageModel.DoesNotExist:
            data_dict = {}
        data_dict.update({'classid': classid})
        return render(request, "manager/content/page.html", data_dict)

    def post(self, request):
        classid = request.GET.get("classid")
        piclist = request.POST.get("piclist")
        content = request.POST.get("content")
        try:
            pageinfo = ModelPageModel.objects.get(cid=classid)
            if pageinfo:
                ModelPageModel.objects.filter(cid=classid).update(content=content, piclist=piclist)
        except ModelPageModel.DoesNotExist:
            ModelPageModel.objects.create(cid=classid, content=content, piclist=piclist)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    

def recycle(request):
    keyword = request.GET.get("keyword", "")
    try:
        content_items = ContentModel.objects.order_by('-lastupdate').filter(islock=-1).filter(title__contains=keyword)
    except ContentModel.DoesNotExist:
        content_items=[]

    for i in range(0, len(content_items)):
        try:
            if content_items[i].classid:
                cateinfo = CategoryModel.objects.get(cateid=content_items[i].classid)
                content_items[i].catename = cateinfo.catename
            else:
                content_items[i].catename = ''

        except ContentModel.DoesNotExist:
            content_items[i].catename = ''

    paginator = Paginator(content_items, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'manager/content/recycle.html', locals())


def lists(request):
    classid = int(request.GET.get("classid", 0))
    # print(classid)
    return render(request, 'manager/content/lists.html', locals())


def delete(request):
    id = request.GET.get("id", 0)
    ContentModel.objects.filter(pk=id).update(islock=-1)

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def clear(request):
    id = request.GET.get("id", 0)
    ContentModel.objects.filter(pk=id).delete()

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def btach(request):
    id = request.POST.get("id", 0)
    type = request.POST.get("type", 0)
    if type == '1':
        ContentModel.objects.filter(id__in=id.split(',')).update(islock=1)
        result = {"state": "success", "msg": "提交成功"}
    if type == '2':
        ContentModel.objects.filter(id__in=id.split(',')).update(islock=0)
        result = {"state": "success", "msg": "提交成功"}
    if type == '3':
        ContentModel.objects.filter(id__in=id.split(',')).update(isnice=1)
        result = {"state": "success", "msg": "提交成功"}
    if type == '4':
        ContentModel.objects.filter(id__in=id.split(',')).update(isnice=0)
        result = {"state": "success", "msg": "提交成功"}
    if type == '5':
        ContentModel.objects.filter(id__in=id.split(',')).update(ontop=1)
        result = {"state": "success", "msg": "提交成功"}
    if type == '6':
        ContentModel.objects.filter(id__in=id.split(',')).update(ontop=0)
        result = {"state": "success", "msg": "提交成功"}
    if type == '7':
        ContentModel.objects.filter(id__in=id.split(',')).update(islock=-1)
        result = {"state": "success", "msg": "提交成功"}
    # result = {"state": "fail", "msg": "保存失败"}
    return JsonResponse(result, safe=False)


def switchs(request):
    id = request.GET.get("id", 0)
    type = request.GET.get("type", 0)
    state = request.POST.get("state", 0)
    if type == '1':
        ContentModel.objects.filter(id=id).update(ontop=state)
        result = {"state": "success", "msg": "提交成功"}
    if type == '2':
        ContentModel.objects.filter(id=id).update(isnice=state)
        result = {"state": "success", "msg": "提交成功"}
    if type == '3':
        ContentModel.objects.filter(id=id).update(islock=state)
        result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def move(request):
    id = request.POST.get("id", 0)
    go = request.POST.get("go", 0)
    ContentModel.objects.filter(id__in=id.split(',')).update(classid=go)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def tree(request):
    classid = request.GET.get('classid', 0)
    zNodes = gen_tree_zNodes(0,[], classid)
    return render(request, 'manager/content/tree.html', locals())


def taglist(request):
    try:
        tags_items = TagsModel.objects.order_by('id').all()
    except TagsModel.DoesNotExist:
        tags_items=[]

    paginator = Paginator(tags_items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'manager/content/tags.html', locals())

def gen_zNodes(pid=0, res=[]):
    cateitems = CategoryModel.objects.filter(followid=pid, catetype__in = [-1, 1, 2, 3])
    if cateitems:
        for cateitem in cateitems:
            if cateitem.catetype == -1:
                url = f'/manager/content/page/?classid={cateitem.cateid}'
            else:
                url = f'/manager/content/lists/?classid={cateitem.cateid}'
            item = dict(
                id = cateitem.cateid,
                name = cateitem.catename,
                pId = cateitem.followid,
                url = url,
                target = 'content_body'
            )
            res.append(item)
            if CategoryModel.objects.filter(followid=cateitem.cateid):
                gen_zNodes(cateitem.cateid, res)
        return res

def gen_tree_zNodes(pid=0, res=[], classid=0):
    cateitems = CategoryModel.objects.filter(followid=pid)
    classinfo = CategoryModel.objects.filter(cateid = classid).first()
    modelid = classinfo.catetype
    if cateitems:
        for cateitem in cateitems:
            sonnum = CategoryModel.objects.filter(followid = cateitem.cateid).count()

            if cateitem.catetype<0:
                chkDisabled = 'true'
            elif cateitem.catetype != modelid:
                chkDisabled = 'true'
            elif cateitem.cateid == classid:
                chkDisabled = 'true'
            elif sonnum != 0:
                chkDisabled = 'true'
            else:
                chkDisabled = 'false'
            item = dict(
                id = cateitem.cateid,
                name = cateitem.catename,
                pId = cateitem.followid,
                open = 'true',
                chkDisabled = chkDisabled,
            )
            res.append(item)
            if CategoryModel.objects.filter(followid=cateitem.cateid):
                gen_tree_zNodes(cateitem.cateid, res, classid)
        return res