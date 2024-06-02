from django import template
from manager.models import ContentModel, CategoryModel
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from django.db.models import Q

register = template.Library()


@register.inclusion_tag("tags/manager/content_lists.html", takes_context=True)
def manager_content_list(context):
    classid = context["request"].GET.get("classid", 0)
    try:
        if classid:
            content_items = ContentModel.objects.order_by('id').filter(Q(islock=0) | Q(islock=1)).filter(classid=classid)
        else:
            content_items = ContentModel.objects.order_by('id').filter(Q(islock=0) | Q(islock=1))
    except ContentModel.DoesNotExist:
        content_items=[]

    # print(content_items)
    for i in range(0, len(content_items)):
        try:
            if content_items[i].classid:
                cateinfo = CategoryModel.objects.get(cateid=content_items[i].classid)
                content_items[i].catename = cateinfo.catename
            else:
                content_items[i].catename = ''
        except CategoryModel.DoesNotExist:
            content_items[i].catename = ''

    paginator = Paginator(content_items, 10)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        "classid": classid,
        'page_obj': page_obj,
        "request": context["request"],
    }