from django.shortcuts import render
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views import View
from manager.models import Admin
from django.core import serializers

# 用户登录
class IndexView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        return render(request, 'manager/login.html', locals())
    def post(self, request):
        adminname = request.POST.get("adminname", None) # 用户提交的验证码
        adminpass = request.POST.get("adminpass", None) # 验证码答案
        captcha = request.POST.get("captcha", None)
        hashkey = request.POST.get("captcha_0", None)
    
        # 用户名密码校验
        if not adminname or not adminpass:
            result = {"state": -1, "msg": "login info error"}
        else:
            admin_info = Admin.objects.filter(adminname=adminname).first()
            if not admin_info:
                result = {"state": -1, "msg": "adminname not found"}
            else:
                if check_password(adminpass, admin_info.adminpass):
                     # 验证码校验
                    if captcha:
                        if not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
                            result = {"state": -1, "msg": "captcha info error"}
                        else:
                            result = {"state": "success", "msg": "登录成功"}
                            request.session["adminid"] = admin_info.adminid
                            
                else:
                    result = {"state": -1, "msg": "adminpass error"}
        return JsonResponse(result, safe=False)
