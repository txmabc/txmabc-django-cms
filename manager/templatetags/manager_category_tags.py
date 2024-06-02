from django import template
from manager.models import CategoryModel
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag("tags/manager/category_list.html", takes_context=True)
def category_list(context):
    fid = context["fid"]
    try:
        category_items = CategoryModel.objects.order_by('catenum').filter(followid=fid)
    except CategoryModel.DoesNotExist:
        category_items=[]
    
    for i in range(0, len(category_items)):
        try:
            child_num = CategoryModel.objects.order_by('catenum').filter(followid=category_items[i].cateid)
            category_items[i].snum = len(child_num)
        except CategoryModel.DoesNotExist:
            category_items[i].snum = 0

    paginator = Paginator(category_items, 10)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        "fid": fid,
        'page_obj': page_obj,
        "request": context["request"],
    }

@register.filter()
def get_page_postion(id):
    id=str(id)
    data = {}
    cateitems = CategoryModel.objects.all()
    if cateitems:
        for cateitem in cateitems:
            item = dict(
                cateid = cateitem.cateid,
                catename = cateitem.catename,
                followid = cateitem.followid,
            )
            data[str(cateitem.cateid)] = item

    tree = []
    while True:
        tree.append(data[id]['cateid'])
        id = str(data[id]['followid'])
        if id == '0':
            break
    tree.reverse()
    mid=' > '
    html=''
    for i in tree:
        html += f'{mid}<a href="?classid={i}">' + data[str(i)]['catename'] + '</a>';
    return html