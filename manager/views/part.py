from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import AdminPart, AdminMenu, CategoryModel
from django.core.paginator import Paginator

import json 
import time

# 添加内容
class IndexView(View):
    def get(self, request):
        try:
            part_items = AdminPart.objects.order_by('ordnum').all()
        except AdminPart.DoesNotExist:
            part_items=[]

        return render(request, "manager/config/admin_part/index.html",locals())

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            AdminPart.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/config/admin_part/add.html", locals())

    def post(self, request):
        AdminPart.objects.create(
            title = request.POST.get("title"),
            pagelever = request.POST.getlist("pagelever", ''),
            ordnum = request.POST.get("ordnum", 0),
            pagelock = request.POST.get("pagelock", 0),
        )
        # result = {"state": "success", "msg": "保存成功"}
        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = AdminPart.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/config/admin_part/edit.html", data_dict)

    def post(self, request, id):
        AdminPart.objects.filter(id=id).update(
            title = request.POST.get("title"),
            pagelever = request.POST.getlist("pagelever", ''),
            ordnum = request.POST.get("ordnum", 0),
            pagelock = request.POST.get("pagelock", 0),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
        
def delete(request, id):
    AdminPart.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)

# 栏目权限
class CateView(View):
    def get(self, request, id):
        cate = gen_tree_zNodes(0, [])
        part_info = AdminPart.objects.get(pk=id)
        cate_list = [int(p) for p in part_info.cate_list.split(',') if part_info.cate_list]
        return render(request, "manager/config/admin_part/cate.html", locals())

    def post(self, request, id):
        cate_list = request.POST.get('cate_list')
        AdminPart.objects.filter(id=id).update(cate_list=cate_list)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 页面权限
class PageView(View):
    def get(self, request, id):
        part_info = AdminPart.objects.get(pk=id)
        page_list = [int(p) for p in part_info.page_list.split(',') if part_info.page_list]
        return render(request, "manager/config/admin_part/page.html", locals())

    def post(self, request, id):
        page_list = request.POST.get('page_list')
        AdminPart.objects.filter(id=id).update(page_list=page_list)
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)
    
def gen_tree_zNodes(pid=0, res=[]):
    cateitems = CategoryModel.objects.filter(followid=pid)
    if cateitems:
        for cateitem in cateitems:
            res.append(cateitem)
            if CategoryModel.objects.filter(followid=cateitem.cateid):
                gen_tree_zNodes(cateitem.cateid, res)
        return res