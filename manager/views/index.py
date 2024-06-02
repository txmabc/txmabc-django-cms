from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from manager.models import Admin, AdminMenu
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, "manager/index.html", locals())

def out(request):
    if request.session.get("adminid"):
        del request.session["adminid"]
    return HttpResponseRedirect(reverse("manager:login"))

def right(request):
    data = {
        "user" : {
            "total" : 21354,
            "num" : 354
        },
        "inquiry" : {
            "total" : 21354,
            "num" : 354
        },
        "order" : {
            "total" : 21354,
            "num" : 354
        },
        "book" : {
            "total" : 21354,
            "num" : 354
        }
    }
    return render(request, "manager/right.html", locals())

class PassView(View):
    def get(self, request):
        return render(request, 'manager/config/admin/pass.html', locals())
    def post(self, request):    
        adminid = request.session.get("adminid")
        oldadminpass = request.POST.get("oldadminpass")
        adminpass = request.POST.get("adminpass")
        readminpass = request.POST.get("readminpass")

        admin = Admin.objects.filter(adminid=adminid).first()
        if not admin:
            result = {"state":  "fail", "msg": "找不到用户"}
        else:
            if not check_password(oldadminpass, admin.adminpass):
                result = {"state":  "fail", "msg": "原密码不正确"}
            else:
                if adminpass == readminpass:
                    Admin.objects.filter(adminid=adminid).update(adminpass = make_password(adminpass))
                    result = {"state":  "success", "msg": "操作成功"}
                else:
                    result = {"state":  "fail", "msg": "两次密码不一致"}
        return JsonResponse(result, safe=False)
