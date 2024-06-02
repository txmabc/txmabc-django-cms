from django.shortcuts import get_object_or_404
from manager.models import ConfigModel, BlockModel


def webconfig(request):
    data_dict = {}
    webinfo = ConfigModel.objects.filter(islock=1).all()
    for item in webinfo:
        newkey = item.ckey.upper()
        data_dict.update({newkey:item.cvalue})
    return data_dict


def webblock(request):
    try:
        block_items = BlockModel.objects.all()
    except BlockModel.DoesNotExist:
        block_items=[]
    webblock = {}
    for block in block_items:
        webblock[block.key] = block.content
    return {'webblock':webblock}