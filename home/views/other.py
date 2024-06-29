from manager.models import TagsModel, ContentModel, Inquiry, Order, ModelProModel, UserModel, UserMoney
from django.core.paginator import Paginator
from django.db.models import Q
import json
from home.function import my_render
import time 
from home.function import get_client_ip
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
import random
import datetime

def taglist(request, id:int):
    catename = "标签"
    encatename = "tags"
    try:
        taginfo = TagsModel.objects.get(pk=id)
    except TagsModel.DoesNotExist:
        taginfo = {'title':''}
    tagname = taginfo.title
    position = [{'name':'标签', 'url':'tags'},{'name': taginfo.title,'url':''}]

    content_items = ContentModel.objects.order_by('ordnum').filter(islock=1).filter(Q(title__contains=tagname)|Q(tags__contains=tagname)).all()
    for content_item in content_items:
        content_item.link = f'/news/show/{content_item.id}.html'
        if content_item.tagslist:
            content_item.tagslist =  json.loads(content_item.tagslist.replace("'", '"'))
        else:
            content_item.tagslist = []
    print(tagname)

    paginator = Paginator(content_items, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return my_render(request, "taglist.html", locals())

def sitemap(request):
    catename = "网站地图"
    encatename = "sitemap"
    return my_render(request, "sitemap.html", locals())

def tags(request):
    catename = "标签"
    encatename = "tags"
    return my_render(request, "tags.html", locals())

class InquiryView(View):
    def post(self, request):
        id = int(request.GET.get("id",0))
        userip=get_client_ip(request)

        #获取IP用户上次提交时间
        rs=Inquiry.objects.raw("select id,createdate from manager_inquiry where postip='%s' order by id desc limit 1"%userip)
        if rs:
            #默认1分钟
            if (time.time() - rs[0].createdate)/60 < 1:
                result = {"state": "fail", "msg": "提交太频繁"}
                return JsonResponse(result, safe=False)
        rs = ModelProModel.objects.raw("select proid,title from manager_modelpromodel left join manager_contentmodel on manager_modelpromodel.cid=manager_contentmodel.id where islock=1 and id=%s limit 1"%id)
        if not rs:
            result = {"state": "fail", "msg": "参数错误"}
            return JsonResponse(result, safe=False)
        d = {}
        d['title'] = rs[0].title
        d['truename'] = request.POST.get("truename")
        d['mobile'] = request.POST.get("mobile")
        d['remark'] = request.POST.get("remark")
        d['isover'] = 0
        d['postip'] = userip
        d['createdate'] = int(time.time())
        Inquiry.objects.create(**d)
        result = {"state": "success", "msg": "操作成功"}
        return JsonResponse(result, safe=False)


class OrdershowView(View):
    def get(self, request, orderid):
        
        catename='订单详情'
        encatename='order details'

        if not orderid:
            return redirect(reverse('home:index'))
        position=[{'name':catename, 'url':reverse('home:other_ordershow', args=[orderid])}]
        rs = Order.objects.filter(orderid=orderid)
        if not rs:
            return redirect(reverse('home:index'))
        userid=rs[0].userid
        umoney=0


        if userid and request.session["user_info"]["id"]:
            if request.session["user_info"]["id"] != userid:
                return redirect(reverse('home:index'))

        ru = UserModel.objects.raw(f"select id,umoney from manager_usermodel where id={userid} limit 1")
        
        if ru:
            umoney = ru[0].umoney
        data_dict = rs[0].__dict__
        data_dict.update({"umoney":umoney, "orderid":orderid})

        return my_render(request, "ordershow.html",data_dict)

    def post(self, request):
        orderid = request.GET.get('orderid')

        # result = {"state": "success", "msg": "保存成功"}
        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


class OrderPayView(View):
    def post(self, request, orderid):
        userid = request.session["user_info"]["id"]
        if not request.session["user_info"]["id"]:
            result = {"state": "fail", "msg": "请先登录或注册"}
            return JsonResponse(result, safe=False)
        rs = Order.objects.raw(f"select id,pro_price,ispay from manager_order where orderid='{orderid}' limit 1")
        if not rs:
            result = {"state": "fail", "msg": "订单编号错误"}
            return JsonResponse(result, safe=False)
        else:
            price=rs[0].pro_price
            if rs[0].ispay:
                result = {"state": "fail", "msg": "订单已付款"}
                return JsonResponse(result, safe=False)
        if price <= 0:
            result = {"state": "fail", "msg": "价格错误"}
            return JsonResponse(result, safe=False)
        rs = UserModel.objects.raw(f"select id,umoney from manager_usermodel where id={userid} limit 1")
        if not rs:
            result = {"state": "fail", "msg": "会员资料不存在"}
            return JsonResponse(result, safe=False)
        oldmoney=rs[0].umoney
        if oldmoney < price:
            result = {"state": "fail", "msg": "余额不足，无法支付！"}
            return JsonResponse(result, safe=False)
        umoney=oldmoney-price

        #扣除
        UserModel.objects.filter(id=userid).update(umoney=umoney)
		#写财务记录
        UserMoney.objects.create(types=2, title=f'订单付款（订单号：{orderid}）', userid=userid, amount=price, oldmoney=oldmoney, newmoney=umoney, createdate=int(time.time()))
		#更新付款状态
        Order.objects.filter(orderid=orderid).update(ispay=1, payway='余额支付')
        
        result = {"state": "success", "msg": "支付成功"}
        return JsonResponse(result, safe=False)

class OrderView(View):
    def post(self, request):
        id = int(request.GET.get('id'))
        userip = get_client_ip(request)
        userid = request.session["user_info"]["id"]
        if not userid:
            result = {"state": "fail", "msg": "请先登录或注册"}
            return JsonResponse(result, safe=False)
        rs = Order.objects.raw(f"select id,createdate from manager_order where postip='{userip}' and userid={userid} order by id desc limit 1")
        if rs:
            if (time.time() - rs[0].createdate)/60 < 1:
                result = {"state": "fail", "msg": "提交太频繁"}

        rs = Order.objects.raw(f"select proid,id,title,price from manager_modelpromodel left join manager_contentmodel on manager_modelpromodel.cid=manager_contentmodel.id where islock=1 and id={id} limit 1")
        if not rs:
            result = {"state": "fail", "msg": "参数错误"}
            return JsonResponse(result, safe=False)

        proname = rs[0].title
        price = rs[0].price
        orderid = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(10000, 99999))

        d={}
        d['pro_name'] = proname
        d['pro_num'] = int(request.POST.get('pronum',0))
        d['pro_price'] = int(request.POST.get('pronum',0))*price
        d['orderid'] = orderid
        d['truename'] = request.POST.get('truename')
        d['mobile'] = request.POST.get('mobile')
        d['address'] = request.POST.get('address')
        d['remark'] = request.POST.get('remark')
        d['ispay'] = 0
        d['isover'] = 0
        d['createdate'] = int(time.time())
        d['postip'] = userip
        d['userid'] = userid

        data = Order.objects.create(**d)
        result = {"state": "success", "msg": reverse('home:other_ordershow', args=[orderid])}
        return JsonResponse(result, safe=False)
    