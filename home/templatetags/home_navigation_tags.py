from django import template
from manager.models import CategoryModel

register = template.Library()

@register.inclusion_tag("tags/home/top_menu.html", takes_context=True)
def home_top_menu(context):
    cate_items = CategoryModel.objects.order_by('catenum').filter(followid=0)
    for cate in cate_items:
        try:
            cate.children = CategoryModel.objects.order_by('catenum').filter(followid=cate.cateid)
        except:
            cate.children = []
    return {
        "cate_items": cate_items,
        "request": context["request"],
    }


@register.inclusion_tag("tags/home/mobile/top_menu.html", takes_context=True)
def home_mobile_top_menu(context):
    cate_items = CategoryModel.objects.order_by('catenum').filter(followid=0)
    for cate in cate_items:
        try:
            cate.children = CategoryModel.objects.order_by('catenum').filter(followid=cate.cateid)
        except:
            cate.children = []
    return {
        "cate_items": cate_items,
        "request": context["request"],
    }

@register.inclusion_tag("tags/home/left_nav.html", takes_context=True)
def home_left_nav(context, topid):

    cate_items = CategoryModel.objects.order_by('catenum').filter(followid=topid)
    for cate in cate_items:
        try:
            cate.children = CategoryModel.objects.order_by('catenum').filter(followid=cate.cateid)
        except:
            cate.children = []
    try:
        topid = context["topid"]
    except:
        topid = 1
    try:
        parentid = context["parentid"]
    except:
        parentid = '0'
    return {
        "topid": topid,
        "parentid": parentid,
        "cate_items": cate_items,
        "request": context["request"],
    }