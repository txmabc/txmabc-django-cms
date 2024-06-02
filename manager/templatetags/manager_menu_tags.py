from django import template
from manager.models import AdminMenu


register = template.Library()

@register.inclusion_tag("tags/manager/left_menu.html", takes_context=True)
def left_menu(context):
    menuitems = AdminMenu.objects.filter(islock=1).filter(followid=0).order_by('ordnum').all()
    return {
        "menuitems": menuitems,
        "request": context["request"],
    }


@register.inclusion_tag("tags/manager/left_menu_children.html", takes_context=True)
def left_menu_children(context, fid):
    menuitems_children = AdminMenu.objects.filter(islock=1).filter(followid=fid).order_by('ordnum').all()
    return {
        "menuitems_children": menuitems_children,
        "request": context["request"],
    }