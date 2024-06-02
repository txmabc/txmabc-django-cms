from django import template
from manager.models import LinkModel
from django.core.paginator import Paginator

import json 

register = template.Library()

# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag("tags/home/link_list.html", takes_context=True)
def home_link_list(context):
    try:
        link_items = LinkModel.objects.filter(islock=1).all()
    except:
        link_items = []
    return {
        "link_items": link_items,
        "request": context["request"],
    }