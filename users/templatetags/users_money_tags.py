from django import template
from manager.models import UserGroupModel, UserMoney
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag("tags/users/users_money_lists.html", takes_context=True)
def users_usermoney_lists(context):
    userid = context['userid']
    types = context['types']
    where = context['where']
    keyword = context['keyword']
    try:
        user_money_items = UserMoney.objects.raw('select * from manager_usermoney a left join manager_usermodel b on a.userid=b.id where ' + where + ' order by a.aid desc')
    except UserMoney.DoesNotExist:
        user_money_items=[]
    
    paginator = Paginator(user_money_items, 20)
    page_number = context["request"].GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return {
        'page_obj': page_obj,
        "request": context["request"],
    }