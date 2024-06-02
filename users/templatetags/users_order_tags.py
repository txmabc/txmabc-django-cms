from django import template
from manager.models import Order
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag("tags/users/users_order_lists.html", takes_context=True)
def users_order_lists(context):
    where = context['where']
    try:
        user_money_items = Order.objects.raw('select * from manager_order where ' + where + ' order by id desc')
    except Order.DoesNotExist:
        user_money_items=[]
    
    paginator = Paginator(user_money_items, 20)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        'page_obj': page_obj,
        "request": context["request"],
    }