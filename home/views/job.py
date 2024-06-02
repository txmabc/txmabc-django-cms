from django.shortcuts import render
from manager.models import ContentModel,CategoryModel,ModelJobModel,JobFormModel
from django.http import JsonResponse
from django.views import View
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore

def lists(request, classid:int):
    data_dict = {}
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    job_items = ContentModel.objects.order_by('ordnum').all()
    data_dict.update({'job_item':job_items})

    return render(request, "home/content/job/list.html", data_dict)

def show(request, id:int):
    data_dict = {}
    job_info = ContentModel.objects.get(id=id)
    ContentModel.objects.filter(pk=id).update(hits=job_info.hits+1)
    job_info.hits += 1
    job_info_dict = job_info.__dict__
    data_dict.update(job_info_dict)

    job_info_extend = ModelJobModel.objects.get(cid=id)
    job_info_extend_dict = job_info_extend.__dict__
    data_dict.update(job_info_extend_dict)

    classid = job_info.classid
    cate_info = CategoryModel.objects.filter(cateid=classid).get()
    cate_info_dict = cate_info.__dict__
    data_dict.update(cate_info_dict)

    parentiditems = get_parent(classid)
    parentid = ','.join(map(str, parentiditems))
    topid = parentiditems[-1]
    data_dict.update({'topid':topid, 'parentid':parentid})

    return render(request, "home/content/job/show.html", data_dict)


# 添加内容
class FormView(View):
    def get(self, request):
        catename = "简历"
        encatename = "resume"
        jobname = request.GET.get('jobname')
        new_captcha = CaptchaStore.generate_key()
        hashkey =  new_captcha
        image_url = captcha_image_url(new_captcha)

        return render(request, "home/content/job/form.html",locals())

    def post(self, request):
        captcha = request.POST.get("captcha", None)
        hashkey = request.POST.get("captcha_0", None)

         # 验证码校验
        if captcha:
            if not CaptchaStore.objects.filter(response=captcha, hashkey=hashkey).count():
                result = {"state": "fail", "msg": "验证码错误"}
            else:
                ip = get_client_ip(request)
                JobFormModel.objects.create(
                    my_title = request.POST.get("my_title"),
                    my_truename = request.POST.get("my_truename"),
                    my_sex = request.POST.get("my_sex"),
                    my_age = request.POST.get("my_age"),
                    my_mobile = request.POST.get("my_mobile"),
                    my_education = request.POST.get("my_education"),
                    my_work_exp = request.POST.get("my_work_exp"),
                    my_intro = request.POST.get("my_intro"),
                    my_ip = ip
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


def get_parent(id:int):
    tree = []
    while id:
        data = CategoryModel.objects.filter(cateid=id).get()
        tree.append(data.cateid)
        id= data.followid
    return tree