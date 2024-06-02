from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import TempMail
import urllib.parse

# 添加内容
def index(request):
    try:
        content_items = TempMail.objects.order_by('id').all()
    except TempMail.DoesNotExist:
        content_items=[]
    return render(request, "manager/theme/mail/index.html",locals())


# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/theme/mail/add.html", locals())

    def post(self, request):
        TempMail.objects.create(
            title = request.POST.get("title"),
            pagelever = request.POST.getlist("pagelever", ''),
            ordnum = request.POST.get("ordnum", 0),
            pagelock = request.POST.get("pagelock", 0),
        )
        # result = {"state": "success", "msg": "保存成功"}
        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)
    

# 编辑内容
class EditView(View):
    def get(self, request, id):
        data_dict = {}
        content_info = TempMail.objects.get(id=id)
        content_dict = content_info.__dict__
        data_dict.update(content_dict)

        return render(request, "manager/theme/mail/edit.html", data_dict)

    def post(self, request, id):
        TempMail.objects.filter(id=id).update(
            title = request.POST.get("title"),
            mail_title = request.POST.get("mail_title"),
            mail_content = request.POST.get("mail_content"),
            islock = request.POST.get("islock", 0),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


def delete(request, id):
    TempMail.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)


def switchs(request, id):
    state = int(request.POST.get("state", 0))
    TempMail.objects.filter(id=id).update(islock=state)

    result = {"state": "success", "msg": "提交成功"}
    return JsonResponse(result, safe=False)