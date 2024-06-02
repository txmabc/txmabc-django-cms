from django import template
from manager.models import CategoryModel,ContentModel,ModelProModel,ModelJobModel
from django.core.paginator import Paginator

import json 

register = template.Library()

# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag("tags/home/job_list.html", takes_context=True)
def home_job_list(context):
    sonid = get_chlid(context['cateid'])
    content_items = ContentModel.objects.order_by('ordnum').filter(classid__in=sonid).all()
    for content_item in content_items:
        pro_info_extend = ModelJobModel.objects.get(cid=content_item.id)
        content_item.work_money = pro_info_extend.work_money
       

        content_item.link = f'/job/show/{content_item.id}.html'
        if content_item.tagslist:
            # print(type(content_item.tagslist))
            content_item.tagslist = content_item.tagslist.replace("'", '"')
            content_item.tagslist =  json.loads(content_item.tagslist)
            
        else:
            content_item.tagslist = []

    paginator = Paginator(content_items, 20)
    page_number = context['request'].GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "request": context["request"],
    }

# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag("tags/home/pro_list.html", takes_context=True)
def home_pro_list(context):
    sonid = get_chlid(context['cateid'])
    content_items = ContentModel.objects.order_by('ordnum').filter(islock=1).filter(classid__in=sonid).all()
    for content_item in content_items:
        pro_info_extend = ModelProModel.objects.get(cid=content_item.id)
        content_item.price = pro_info_extend.price
       
        content_item.link = f'/product/show/{content_item.id}.html'
        if content_item.tagslist:
            # print(type(content_item.tagslist))
            content_item.tagslist = content_item.tagslist.replace("'", '"')
            content_item.tagslist =  json.loads(content_item.tagslist)
        else:
            content_item.tagslist = []

    paginator = Paginator(content_items, 20)
    page_number = context['request'].GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "request": context["request"],
    }


@register.inclusion_tag("tags/home/mobile/pro_list.html", takes_context=True)
def home_mobile_pro_list(context):
    sonid = get_chlid(context['cateid'])
    content_items = ContentModel.objects.order_by('ordnum').filter(islock=1).filter(classid__in=sonid).all()
    for content_item in content_items:
        pro_info_extend = ModelProModel.objects.get(cid=content_item.id)
        content_item.price = pro_info_extend.price
       
        content_item.link = f'/product/show/{content_item.id}.html'
        if content_item.tagslist:
            # print(type(content_item.tagslist))
            content_item.tagslist = content_item.tagslist.replace("'", '"')
            content_item.tagslist =  json.loads(content_item.tagslist)
        else:
            content_item.tagslist = []

    paginator = Paginator(content_items, 20)
    page_number = context['request'].GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "request": context["request"],
    }


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