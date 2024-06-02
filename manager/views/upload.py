from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import Attachment
import os
from django.conf import settings
import datetime
import random
from django.views.decorators.csrf import csrf_exempt

# 上传图片
def imageupload(request, type=1, multiple=0, gid=0):
    return render(request, 'manager/other/upload.html', locals())

# 选择图片
def imagelist(request, type=1, multiple=0):
    gid = request.GET.get('gid', 0)
    thumb=1
    water=1
    islocal=0
    iseditor = 0
    keyword = request.GET.get('keyword', '')
    return render(request, 'manager/other/image.html', locals())

def uploadfile(request):
    # file_url url             地址
    # file_name                文件名
    # file_ext                 文件后缀
    # file_size                文件大小
    # file_type                文件类型（1：图片，2：视频，3：其他） 默认0
    # file_update              上传的日期 默认当前日期 
    # file_local               存放位置（1：本地，2：阿里云，3：七牛云） 默认0
    # file_adminid             管理员id 默认0
    # file_userid              用户id 默认0
    # file_ip                  上传者IP 默认null
    # gid                      分组id 默认0 未分组

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
    file_userid = 0
    file_ip = request.META['REMOTE_ADDR']
    gid = request.GET.get('gid', 0)

    file_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    file_dir = os.path.join(settings.MEDIA_ROOT, file_date)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_new_name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(10000, 99999)) + file_ext
    file_path = f"{file_dir}/{file_new_name}"
    file_url=f'{settings.MEDIA_URL}{file_date}/{file_new_name}'

    handle_uploaded_file(file, file_path)
    Attachment.objects.create(file_url=file_url, file_name=file_name, file_ext=file_ext, file_type=file_type, file_local=file_local, file_adminid=file_adminid, file_userid=file_userid, file_ip=file_ip, gid=gid)
    
    result = {"state": "success", "msg": file_url}
    return JsonResponse(result, safe=False)

def upload_tinymce(request):
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
    file_userid = 0
    file_ip = request.META['REMOTE_ADDR']
    gid = 0

    file_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    file_dir = os.path.join(settings.MEDIA_ROOT, file_date)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_new_name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(10000, 99999)) + file_ext
    file_path = f"{file_dir}/{file_new_name}"
    file_url=f'{settings.MEDIA_URL}{file_date}/{file_new_name}'

    handle_uploaded_file(file, file_path)
    Attachment.objects.create(file_url=file_url, file_name=file_name, file_ext=file_ext, file_type=file_type, file_local=file_local, file_adminid=file_adminid, file_userid=file_userid, file_ip=file_ip, gid=gid)
    
    result = {"location": file_url}
    return JsonResponse(result, safe=False)

# 供editor.md上传图片使用接口
from django.views.decorators.clickjacking import xframe_options_deny, xframe_options_sameorigin, xframe_options_exempt
@csrf_exempt
def upload_editor(request):
    file = request.FILES["editormd-image-file"]
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
    file_userid = 0
    file_ip = request.META['REMOTE_ADDR']
    gid = 0

    file_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    file_dir = os.path.join(settings.MEDIA_ROOT, file_date)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_new_name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(10000, 99999)) + file_ext
    file_path = f"{file_dir}/{file_new_name}"
    file_url=f'{settings.MEDIA_URL}{file_date}/{file_new_name}'

    handle_uploaded_file(file, file_path)
    Attachment.objects.create(file_url=file_url, file_name=file_name, file_ext=file_ext, file_type=file_type, file_local=file_local, file_adminid=file_adminid, file_userid=file_userid, file_ip=file_ip, gid=gid)
    
    result = {"success":1, "url": file_url}
    return JsonResponse(result, safe=False)


def handle_uploaded_file(f,file_url):
    with open(file_url, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)