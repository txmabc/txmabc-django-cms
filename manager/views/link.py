from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import LinkModel, ConfigModel, ConfigGroupModel
from django.core.paginator import Paginator
import json
from django.db.models import Q
import os
from django.conf import settings

class IndexView(View):
    def get(self, request):
        try:
            content_items = LinkModel.objects.order_by('ordnum').all()
        except LinkModel.DoesNotExist:
            content_items=[]

        paginator = Paginator(content_items, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request,"manager/extend/link/index.html", locals())

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            LinkModel.objects.filter(pk=mid[i]).update(ordnum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class AddView(View):
    def get(self, request):
        return render(request,"manager/extend/link/add.html", locals())

    def post(self, request):
        data = {
            'webname': request.POST.get('webname'),
            'weblogo': request.POST.get('weblogo'),
            'weburl': request.POST.get('weburl'),
            'classid': request.POST.get('classid'),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        LinkModel.objects.create(**data)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


class EditView(View):
    def get(self, request, id):
        content_info = LinkModel.objects.get(id=id)
        data_dict = content_info.__dict__

        return render(request,"manager/extend/link/edit.html", data_dict)

    def post(self, request, id):
        data = {
            'webname': request.POST.get('webname'),
            'weblogo': request.POST.get('weblogo'),
            'weburl': request.POST.get('weburl'),
            'classid': request.POST.get('classid'),
            'ordnum': request.POST.get('ordnum', 0),
            'islock': request.POST.get('islock', 0),
        }
        LinkModel.objects.filter(pk=id).update(**data)

        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


class ConfigView(View):
    def get(self, request):
        config_info = ConfigGroupModel.objects.filter(islock=1).filter(gkey='link').get()
        return render(request,"manager/extend/link/config.html", locals())

    def post(self, request, id):
        config_list = ConfigModel.objects.filter(gid=id).filter(~Q(ctype=9)).all()
        for item in config_list:
            if item.ctype == 5:
                cvalue = request.POST.get(item.ckey)
                cvalue = cvalue.replace('\r\n', '\n').split('\n')
                cvalue = ','.join(cvalue)
                ConfigModel.objects.filter(ckey=item.ckey).update(cvalue=cvalue)
            else:
                ConfigModel.objects.filter(ckey=item.ckey).update(cvalue=request.POST.get(item.ckey))
        result = {"state": "success", "msg": "保存成功"}

        file_content = ""
        rs = ConfigModel.objects.raw("select id,ckey,cvalue from manager_configmodel where islock=1 and ctype<9 order by ordnum,id")
        
        for c in rs:
            file_content += f'\n{c.ckey.upper()} = "{c.cvalue}"'

         # 设置文件路径
        file_path = os.path.join(settings.BASE_DIR / 'conf', 'config_settings.py')

        # 尝试创建并写入文件
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
            print("文件创建并写入成功。")
        except IOError as e:
            print(f"文件创建或写入失败: {e}")

        return JsonResponse(result, safe=False)
    

def switchs(request, id):
    # id = request.GET.get("id", 0)
    islock = request.POST.get("islock", 0)
    LinkModel.objects.filter(id=id).update(islock=islock)
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)


def delete(request, id):
    # id = request.GET.get("id", 0)
    # islock = request.POST.get("islock", 0)
    LinkModel.objects.filter(id=id).delete()
    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)