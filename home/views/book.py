from django.shortcuts import render
from manager.models import BookModel
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse
from django.views import View


# 添加内容
class IndexView(View):
    def get(self, request):
        catename = "反馈留言"
        encatename = "Feedback"
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)

        return render(request, "home/book.html",locals())

    def post(self, request):
        captcha = request.POST.get("captcha", None)
        hashkey = request.POST.get("captcha_0", None)

         # 验证码校验
        if captcha:
            if not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
                result = {"state": "fail", "msg": "验证码错误"}
            else:
                ip = get_client_ip(request)
                BookModel.objects.create(
                    truename = request.POST.get("truename"),
                    mobile = request.POST.get("mobile"),
                    tel = request.POST.get("tel"),
                    remark = request.POST.get("remark"),
                    postip = ip
                )
                result = {"state": "success", "msg": "保存成功"}
                return JsonResponse(result, safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip