from django import template
from manager.models import Inquiry
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from django.db.models import Q

register = template.Library()

@register.inclusion_tag("tags/manager/inquiry_lists.html", takes_context=True)
def manager_inquiry_list(context):
    types = context["types"]
    where = context["where"]
    keyword = context["keyword"]

    try:
        content_items = Inquiry.objects.raw("select * from manager_inquiry where %s order by id desc"%where)
    except Inquiry.DoesNotExist:
        content_items=[]

    paginator = Paginator(content_items, 10)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        'page_obj': page_obj,
        "request": context["request"],
    }