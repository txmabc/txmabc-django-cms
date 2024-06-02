from django.shortcuts import render
from django.http import JsonResponse
from manager.models import UserMoney, UserModel
from django.core.paginator import Paginator
from django.views import View
import time
import decimal

# 添加内容
def index(request):

    atype = int(request.GET.get('type', 0))
    keyword = request.GET.get('keyword')
    where = '1=1'
    if keyword:
        where +="and (uname like binary '%" + keyword + "%' or title like binary '%" + keyword + "%')"
    if atype == 1:
        where +=' and types=' + str(atype) + ' '
    if atype == 2:
        where +=' and types=' + str(atype) + ' '

    return render(request, "manager/user/money/index.html",locals())

# 添加内容
class AddView(View):
    def get(self, request):
        return render(request, "manager/user/money/add.html", locals())

    def post(self, request):
        username = request.POST.get('username')
        title = request.POST.get('title')
        if not username:
            result = {"state": "fail", "msg": "用户名不能为空"}
            return JsonResponse(result, safe=False)
        if not title:
            result = {"state": "fail", "msg": "备注不能为空"}
            return JsonResponse(result, safe=False)
        userid = 0
        umoney = 0
        
		#检查用户名是否存在
        rs=UserModel.objects.filter(uname=username).get()
        if not rs:
            result = {"state": "fail", "msg": "用户名不存在，请检查"}
            return JsonResponse(result, safe=False)

        userid=rs.id
        umoney=rs.umoney
        oldmoney=umoney

        if int(request.POST.get('type', 2)) == 2:
            if umoney < decimal.Decimal(request.POST.get('amount')):
                result = {"state": "fail", "msg": "用户余款不足，无法完成扣款"}
                return JsonResponse(result, safe=False)
            else:
                umoney= umoney - decimal.Decimal(request.POST.get('amount'))
        else:
            umoney = umoney + decimal.Decimal(request.POST.get('amount'))
       
        d={}
        d['userid'] = userid
        d['amount'] = decimal.Decimal(request.POST.get('amount'))
        d['types'] = int(request.POST.get('type', 2))
        d['title'] = request.POST.get('title')
        d['oldmoney'] = oldmoney
        d['newmoney'] = umoney
        d['createdate'] = int(time.time())
        UserMoney.objects.create(**d)
        UserModel.objects.filter(id=userid).update(umoney=umoney)

        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


def delete(request, id):
    UserMoney.objects.filter(pk=id).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)