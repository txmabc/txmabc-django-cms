from django import template
from manager.models import AdminMenu

register = template.Library()


@register.inclusion_tag("tags/manager/page_menu.html", takes_context=True)
def page_menu(context):
    menuitems = AdminMenu.objects.filter(islock=1).filter(followid=0).order_by('ordnum').all()
    return {
        "page_list": context['page_list'],
        "menuitems": menuitems,
        "request": context["request"],
    }


@register.inclusion_tag("tags/manager/page_menu_children.html", takes_context=True)
def page_menu_children(context, fid):
    menuitems_children = AdminMenu.objects.filter(islock=1).filter(followid=fid).order_by('ordnum').all()
    return {
        "page_list": context['page_list'],
        "menuitems_children": menuitems_children,
        "request": context["request"],
    }