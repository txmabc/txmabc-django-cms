from django import template
from manager.models import ConfigGroupModel,ConfigModel

register = template.Library()


@register.inclusion_tag("tags/manager/config_tab.html", takes_context=True, name="config_tab")
def config_tab(context, gkey):
    config_group = ConfigGroupModel.objects.filter(islock=1).filter(gkey='0').filter(types=1).order_by('ordnum').all()
    config_group_one = ConfigGroupModel.objects.filter(islock=1).filter(id=context["id"]).order_by('ordnum').all()
    return {
        "id": context["id"],
        "config_group": config_group,
        "config_group_one": config_group_one,
        "request": context["request"],
    }


@register.inclusion_tag("tags/manager/config_group_children.html", takes_context=True)
def config_group_children(context, gid):
    config_items = ConfigModel.objects.filter(islock=1).filter(gid=gid).order_by('ordnum').all()
    print(gid)
    return {
        "config_items": config_items,
        "request": context["request"],
    }