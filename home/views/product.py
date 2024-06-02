from django.shortcuts import render
from manager.models import ContentModel,CategoryModel,ModelProModel
import json
from home.function import my_render

def lists(request, classid:int):
    data_dict = {}
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    product_items = ContentModel.objects.order_by('ordnum').all()
    data_dict.update({'product_item':product_items})

    parentiditems = get_parent(classid)
    parentid = ','.join(map(str, parentiditems))
    topid = parentiditems[-1]
    data_dict.update({'topid':topid, 'parentid': parentid})

    return my_render(request, "content/product/list.html", data_dict)


def show(request, id:int):
    data_dict = {}
    product_info = ContentModel.objects.get(pk=id)
    ContentModel.objects.filter(pk=id).update(hits=product_info.hits+1)
    product_info.hits += 1
    product_info_dict = product_info.__dict__
    data_dict.update(product_info_dict)

    product_info_extend = ModelProModel.objects.get(cid=id)
    product_info_extend_dict = product_info_extend.__dict__
    data_dict.update(product_info_extend_dict)

    if product_info_extend_dict['piclist']:
        picdata = json.loads(product_info_extend_dict['piclist'])
        data_dict.update({'picdata': picdata})

    classid = product_info.classid
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    parentiditems = get_parent(classid)
    parentid = ','.join(map(str, parentiditems))
    topid = parentiditems[-1]
    data_dict.update({'topid':topid, 'parentid':parentid})

    return my_render(request, "content/product/show.html", data_dict)

def get_parent(id:int):
    tree = []
    while id:
        data = CategoryModel.objects.filter(cateid=id).get()
        tree.append(data.cateid)
        id= data.followid
    return tree