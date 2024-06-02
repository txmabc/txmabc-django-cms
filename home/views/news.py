from django.shortcuts import render
from manager.models import ContentModel,CategoryModel,ModelNewsModel
from django.core.paginator import Paginator
import json 
import time
from utils.wmcms_page import WmcmsPage
from home.function import my_render

def lists(request, classid:int):
    data_dict = {}
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    parentiditems = get_parent(classid)
    parentid = ','.join(map(str, parentiditems))
    sonid = get_chlid(classid)
    topid = parentiditems[-1]
    data_dict.update({'topid':topid, 'parentid':parentid})

    content_items = ContentModel.objects.order_by('ordnum').filter(islock=1).filter(classid__in=sonid).all()
    for content_item in content_items:
        content_item.link = f'/news/show/{content_item.id}.html'
        if content_item.tagslist:
            # print(type(content_item.tagslist))
            content_item.tagslist = content_item.tagslist.replace("'", '"')
            content_item.tagslist =  json.loads(content_item.tagslist)
            
        else:
            content_item.tagslist = []
        # print(content_item.tagslist)

    paginator = Paginator(content_items, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data_dict.update({'page_obj':page_obj})

    # wmpage = WmcmsPage(request, 1000, 10, 100, 5)
    # print(wmpage.showpage(5))


    return my_render(request, "content/news/list.html", data_dict)

def show(request, id:int):
    data_dict = {}
    news_info = ContentModel.objects.get(pk=id)
    ContentModel.objects.filter(pk=id).update(hits=news_info.hits+1)
    news_info.hits += 1
    news_info_dict = news_info.__dict__
    data_dict.update(news_info_dict)

    news_info_extend = ModelNewsModel.objects.get(cid=id)
    news_info_extend_dict = news_info_extend.__dict__
    data_dict.update(news_info_extend_dict)

    classid = news_info.classid
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    parentiditems = get_parent(classid)
    parentid = ','.join(map(str, parentiditems))
    sonid = get_chlid(classid)
    topid = parentiditems[-1]
    data_dict.update({'topid':topid, 'parentid':parentid})

    return my_render(request, "content/news/show.html", data_dict)


def get_parent(id:int):
    tree = []
    while id:
        data = CategoryModel.objects.filter(cateid=id).get()
        tree.append(data.cateid)
        id= data.followid
    return tree

def get_chlid(id:int):
    subs=[]
    subs.append(id)
    no_subs = []
    while True:
        xlen = len(subs)
        items = CategoryModel.objects.filter(followid__in=subs).exclude(cateid__in=no_subs).all()
        for item in items:
            subs.append(item.cateid)
            no_subs.append(item.cateid)
        if not len(subs) > xlen:
            break
    return subs
	#     do{
	#         $len=count($subs);
	#         foreach($data as $item)
	#         {
	#             if(in_array($item['followid'],$subs))
	#             {
	#                 $subs[]=$item['cateid'];
	#                 unset($data[$item['cateid']]);
	#             }
	#         }
	#     }
	#     while(count($subs)>$len);
	# 	return implode(',', $subs)