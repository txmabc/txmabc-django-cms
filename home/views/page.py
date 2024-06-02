from django.shortcuts import render
from manager.models import ContentModel, CategoryModel, ModelPageModel
import json
from home.function import my_render

def page(request, classid:int):
    data_dict = {}
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    try:
        cate_extend = ModelPageModel.objects.filter(cid=classid).get()
        data_dict.update({'piclist':cate_extend.piclist, 'content':cate_extend.content})   
    except:
        data_dict.update({'piclist':[], 'content':''})

    if data_dict['piclist']:
        picdata = json.loads(data_dict['piclist'])
        data_dict.update({'picdata': picdata})

    parentitems = get_parent(classid)
    parentid = ','.join(map(str, parentitems))
    topid = parentitems[-1]
    data_dict.update({'parentid':parentid, 'topid':topid})

    print(data_dict)
    return my_render(request, "content/page/page.html", data_dict)

def get_parent(id:int):
    tree = []
    while id:
        data = CategoryModel.objects.filter(cateid=id).get()
        tree.append(data.cateid)
        id= data.followid
    return tree