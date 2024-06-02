from django import template
from manager.models import Order
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from django.db.models import Q

register = template.Library()

@register.inclusion_tag("tags/manager/order_lists.html", takes_context=True)
def manager_order_list(context):
    type = context["type"]
    where = context["where"]
    keyword = context["keyword"]

    if keyword:
        where += " and (orderid like binary '%" + keyword + "%' or truename like binary '%" + keyword + "%' or mobile like binary '%" + keyword + "%')"
    print(type)
    if type == 1:
        where +=' and ispay=0'
    if type == 2:
        print(type)
        where +=' and ispay=1'
    if type == 3:
        where +=' and isover=0'
    if type == 4:
        where +=' and isover=1'
    if type == 0:
        pass

    try:
        content_items = Order.objects.raw("select * from manager_order where %s order by id desc"%where)
    except Order.DoesNotExist:
        content_items=[]

    paginator = Paginator(content_items, 10)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        'page_obj': page_obj,
        "request": context["request"],
    }