from django import template
from manager.models import UserGroupModel, UserMoney
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag("tags/manager/user_group.html", takes_context=True)
def user_group(context):
    try:
        user_group_items = UserGroupModel.objects.order_by('ordnum').all()
    except UserGroupModel.DoesNotExist:
        user_group_items=[]
    
    return {
        'user_group_items': user_group_items,
        "request": context["request"],
    }

@register.inclusion_tag("tags/manager/user_group_edit.html", takes_context=True)
def user_group_edit(context):
    try:
        user_group_items = UserGroupModel.objects.order_by('ordnum').all()
    except UserGroupModel.DoesNotExist:
        user_group_items=[]
    categroup_items = []
    if context['categroup']:
        if ',' in context['categroup']:
            categroup_items = context['categroup'].split(",")
        else:
            categroup_items = [context['categroup']]
    else:
        categroup_items = []

    return {
        'user_group_items': user_group_items,
        'categroup_items': categroup_items,
        "request": context["request"],
    }

@register.inclusion_tag("tags/manager/user_group_view_lever.html", takes_context=True)
def user_group_view_lever(context):
    try:
        user_group_items = UserGroupModel.objects.order_by('ordnum').all()
    except UserGroupModel.DoesNotExist:
        user_group_items=[]

    try:
        view_groupid = [int(p) for p in context['view_groupid'].split(',')]
    except:
        view_groupid = []
    print(view_groupid)
    return {
        'view_groupid': view_groupid,
        'user_group_items': user_group_items,
        "request": context["request"],
    }


@register.inclusion_tag("tags/manager/user_money_lists.html", takes_context=True)
def manager_usermoney_lists(context):
    atype = context['atype']
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