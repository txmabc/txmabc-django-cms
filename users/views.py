from django.shortcuts import render
from users.serializers import UserSerializers
import datetime
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views import View
from manager.models import UserModel, UserGroupModel, Attachment
import json
import os
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf import settings
import random

def index(request):
    catename = "会员中心"
    encatename = "Center"
    strTimeToString="000111222334455556666667"
    strWenhou=['夜深了！','凌晨了！','早上好！','上午好！','中午好！','下午好！','晚上好！','夜深了！']
    welcome = strWenhou[int(strTimeToString[int(datetime.datetime.now().strftime('%#H'))])]
    user = UserModel.objects.filter(id=request.session["user_info"]["id"]).first()
    group = UserGroupModel.objects.get(gid=user.uid)
    # print(group.gid)
    user.gname = group.gname

    return render(request, "users/index.html", locals())

def myorder(request):
    catename = "我的订单"
    encatename = "Order"

    types=int(request.GET.get('type', 0))
    userid=request.session['user_info']['id']
    where=f"userid={userid}"
    if types == 1:
        where += ' and ispay=1'
    if types == 2:
        where += ' and ispay=0'
       
    return render(request, "users/myorder.html", locals())

def mymoney(request):
    catename = "财务明细"
    encatename = "Money"

    types = int(request.GET.get('type', 0))
    userid = request.session["user_info"]["id"]
    where = "userid=%s"%userid
    if types == 1:
        where += ' and types=1'
    if types == 2:
        where += ' and types=2'
    keyword=request.GET.get('keyword', '')
    if keyword:
        where += " and title like binary '%" + keyword +"%'"
        
    return render(request, "users/mymoney.html", locals())

# 用户注册
class RegisterView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "用户注册"
        encatename = "Register"
        return render(request, 'users/reg.html', locals())
    def post(self, request):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        repass = request.POST.get("repass", None) 
        uemail = request.POST.get("email", None) 
        captcha = request.POST.get("captcha", None)
        hashkey = request.POST.get("captcha_0", None)

        if not username or not password:
            result = {"state": "fail", "msg": "用户名或密码不能为空"}
        elif password != repass:
            result = {"state": "fail", "msg": "两次密码不一致"}
        elif not captcha:
            result = {"state": "fail", "msg": "验证码不能为空"}
        elif not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
            result = {"state": "fail", "msg": "验证码错误"}
        elif UserModel.objects.filter(uname=username).exists():
            result = {"state": "fail", "msg": "用户名已存在"}
        else:
            data = {
                "uname": username,
                "upass": make_password(password),
                "uemail": uemail,
                "regip": get_client_ip(request),
                "uid": 1,
            }
            UserModel.objects.create(**data)
            result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 用户登录
class LoginView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "用户登录"
        encatename = "Login"
        return render(request, 'users/login.html', locals())
    def post(self, request):
        username = request.POST.get("username", None) # 用户提交的验证码
        password = request.POST.get("password", None) # 验证码答案
        captcha = request.POST.get("captcha", None)
        hashkey = request.POST.get("captcha_0", None)
    
        # 用户名密码校验
        if not username or not password:
            result = {"state": "fail", "msg": "用户名或密码不能为空"}
        else:
            user = UserModel.objects.filter(uname=username).first()
            if not user:
                result = {"state":"fail", "msg": "用户名不存在"}
            else:
                if check_password(password, user.upass):
                     # 验证码校验
                    if captcha:
                        if not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
                            result = {"state": "fail", "msg": "验证码信息错误"}
                        else:
                            result = {"state": "success", "msg": "登录成功"}
                            serializers = UserSerializers(user)
                            request.session["user_info"] = serializers.data
                else:
                    result = {"state": "fail", "msg": "密码错误"}
        return JsonResponse(result, safe=False)


# 用户登出
class LogoutView(View):
    def get(self, request):
        if "user_info" in request.session:
            del request.session["user_info"]
        return redirect(reverse('users:login'))


# 用户信息
class UserInfoView(View):
    def post(self, request):
        user_info = request.session.get("user_info")
        if user_info:
            result = {"code": 0, "msg": f"登录用户为{user_info.uname}"}
            status = 200
        else:
            result = {"code": -1, "msg": "用户未登录"}
            status = 401
        return JsonResponse(result, status=status)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# 忘记密码
class GetpassView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "忘记密码"
        encatename = "Getpass"
        return render(request, 'users/getpass.html', locals())
    def post(self, request):
        result = {"state": "fail", "msg": "操作失败"}
        return JsonResponse(result, safe=False)
    
# 修改邮箱
class EditemailView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "修改邮箱"
        encatename = "Editemail"
        return render(request, 'users/editemail.html', locals())
    def post(self, request):
        result = {"state": "fail", "msg": "操作失败"}
        return JsonResponse(result, safe=False)
    
# 修改密码
class EditpassView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "修改密码"
        encatename = "Editepass"
        return render(request, 'users/editpass.html', locals())
    def post(self, request):
        result = {"state": "fail", "msg": "操作失败"}
        return JsonResponse(result, safe=False)

# 在线支付
class PayView(View):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)
        catename = "在线充值"
        encatename = "online recharge"
        userid = request.session['user_info']['id']
        position=[{'name':'会员中心','url':reverse('users:index')},{'name':catename,'url':reverse('users:pay')}]
 
        return render(request, 'users/pay.html', locals())
    def post(self, request):
        result = {"state": "fail", "msg": "操作失败"}
        return JsonResponse(result, safe=False)
    
def face(request):
    file = request.FILES["file"]
    res = os.path.splitext(file.name)
    file_name = file.name
    file_ext = res[1]
    file_size = file.size
    if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
        file_type = 1
    elif file_ext in ['.mp4']:
        file_type = 2
    else:
        file_type = 3
    file_local = 1
    file_adminid = 0
    file_userid = request.session.get('user_info')['id']
    file_ip = request.META['REMOTE_ADDR']
    gid = 0

    file_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    file_dir = os.path.join(settings.MEDIA_ROOT, file_date)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_new_name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(10000, 99999)) + file_ext
    file_path = f"{file_dir}/{file_new_name}"
    file_url=f'{settings.MEDIA_URL}{file_date}/{file_new_name}'

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    Attachment.objects.create(file_url=file_url, file_name=file_name, file_ext=file_ext, file_type=file_type, file_local=file_local, file_adminid=file_adminid, file_userid=file_userid, file_ip=file_ip, gid=gid)
    UserModel.objects.filter(id=request.session.get('user_info')['id']).update(uface=file_url)
    
    a = request.session.get('user_info')
    a["uface"] = file_url
    request.session["user_info"] = a

    result = {"state": "success", "msg": file_url}
    return JsonResponse(result, safe=False)