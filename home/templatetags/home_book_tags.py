from django import template
from manager.models import BookModel
from django.core.paginator import Paginator

import json 

register = template.Library()

# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag("tags/home/book_list.html", takes_context=True)
def home_book_list(context):
    content_items = BookModel.objects.filter(islock=1).all()

    paginator = Paginator(content_items, 20)
    page_number = context['request'].GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "request": context["request"],
    }