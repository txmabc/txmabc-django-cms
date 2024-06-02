from django.shortcuts import render
from manager.models import AdvertModel, ModelNewsModel, ContentModel
from django.db import connection
import json 
from home.function import my_render

def index(request):
    advert_info = AdvertModel.objects.get(akey="pc")
    if advert_info.datalist:
        advert_list = json.loads(advert_info.datalist)
    
    banner_news_list = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT Content.id,Content.title,Content.createdate FROM manager_modelnewsmodel News LEFT JOIN manager_contentmodel Content ON Content.id=News.cid WHERE Content.islock = 1")
        banner_news_list = dictfetchall(cursor)
    # print(banner_news_list)

    return my_render(request, "index.html", {
        "banner_news_list": banner_news_list,
        "advert_list": advert_list,
        "request": request,
    })


def page(request):
    return render(request, "home/content/page/page.html", locals())


def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]