from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import ConfigModel
from django.shortcuts import get_object_or_404
from django.db.models import Q

# 用户登录
class IndexView(View):
    def get(self, request, id=1):
        return render(request, 'manager/config/config.html', locals())
    def post(self, request, id=1):
        config_list = ConfigModel.objects.filter(gid=id).filter(~Q(ctype=9)).all()
        for item in config_list:
            ConfigModel.objects.filter(ckey=item.ckey).update(cvalue=request.POST.get(item.ckey))
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)