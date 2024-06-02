from django import template
from manager.models import AttachmentGroup, Attachment
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag("tags/manager/attachment_group.html", takes_context=True)
def attachment_group(context):
    attachment_group_items = get_list_or_404(AttachmentGroup, islock=1)
    print(attachment_group_items)
    return {
        "attachment_group_list": attachment_group_items,
        "request": context["request"],
    }

@register.inclusion_tag("tags/manager/attachment_choose_group.html", takes_context=True)
def attachment_choose_group(context):
    attachment_group_items = get_list_or_404(AttachmentGroup, islock=1)
    return {
        "attachment_group_list": attachment_group_items,
        "request": context["request"],
    }

@register.inclusion_tag("tags/manager/attachment_list.html", takes_context=True)
def attachment_list(context):
    gid = context["request"].GET.get("gid", 0)
    
    attachment_group_items = get_list_or_404(AttachmentGroup, islock=1)

    try:
        attachment_items = Attachment.objects.order_by('-file_update').filter(gid=gid)
        # print(attachment_items)
    except Attachment.DoesNotExist:
        attachment_items=[]

    paginator = Paginator(attachment_items, 6)
    page_number = context["request"].GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return {
        "gid": gid,
        "attachment_group_list": attachment_group_items,
        'page_obj': page_obj,
        "request": context["request"],
    }