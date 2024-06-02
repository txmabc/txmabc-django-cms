from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from manager.models import CategoryModel
from manager.function import get_parent, get_depth, get_sonid
import os
from django.conf import settings
from manager.serializers import CategorySerializers

class IndexView(View):
    def get(self, request):
        if not request.GET.get('fid'):
            fid=0
        else:
            fid = int(request.GET.get('fid'))
        try:
            pid = CategoryModel.objects.order_by('catenum').get(cateid=fid).followid
        except:
            pid = 0
        return render(
            request,
            "manager/category/index.html",
            {"request": request, "fid": fid, "pid": pid},
        )

    def post(self, request):
        mid = request.POST.getlist("mid[]")
        ordnum = request.POST.getlist("ordnum[]")
        for i in range(0, len(mid)):
            CategoryModel.objects.filter(pk=mid[i]).update(catenum=ordnum[i])
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


# 添加栏目
class AddView(View):
    def get(self, request):
        fid = int(request.GET.get("fid"))
        return render(
            request, "manager/category/add.html", {"request": request, "fid": fid}
        )

    def post(self, request):
        way = request.POST.get("way")
        if way == "1":
            CategoryModel.objects.create(
                followid = request.GET.get("fid", 0),
                catename = request.POST.get("catename"),
                catetype = request.POST.get("catetype"),
                cateurl = request.POST.get("cateurl"),
                catepage = request.POST.get("catepage"),
                catenum = request.POST.get("catenum"),
                catetitle = request.POST.get("catetitle"),
                catekey = request.POST.get("catekey"),
                catedesc = request.POST.get("catedesc"),
                catelist = request.POST.get("catelist"),
                cateshow = request.POST.get("cateshow"),
                isshow = request.POST.get("isshow", 0),
                isblank = request.POST.get("isblank", 0),
                isfilter = request.POST.get("isfilter", 0),
            )
            result = {"state": "success", "msg": "保存成功"}
            return JsonResponse(result, safe=False)

        result = {"state": "fail", "msg": "保存失败"}
        return JsonResponse(result, safe=False)


# 编辑栏目
class EditView(View):
    def get(self, request):
        fid = int(request.GET.get("fid"))
        cateid = request.GET.get("id")
        cateinfo = CategoryModel.objects.get(cateid=cateid)
        cateinfo_dict = cateinfo.__dict__
        return render(request, "manager/category/edit.html", cateinfo_dict)

    def post(self, request):
        id = int(request.GET.get("id"))
        CategoryModel.objects.filter(pk=id).update(
            catename=request.POST.get("catename"),
            followid = request.GET.get("fid"),
            catetype=request.POST.get("catetype"),
            cateurl=request.POST.get("cateurl"),
            catepage=request.POST.get("catepage"),
            catenum=request.POST.get("catenum"),
            catetitle=request.POST.get("catetitle"),
            catekey=request.POST.get("catekey"),
            catedesc=request.POST.get("catedesc"),
            catelist=request.POST.get("catelist"),
            cateshow=request.POST.get("cateshow"),
            isshow=request.POST.get("isshow", 0),
            isblank=request.POST.get("isblank", 0),
            isfilter=request.POST.get("isfilter", 0),
            parentid = get_parent(id),
            sonid = get_sonid(id),
            depth = get_depth(id),
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)

# 编辑栏目
class MoveView(View):
    def get(self, request):
        id = int(request.GET.get("id"))
        cateinfo = CategoryModel.objects.get(cateid=id)
        catename = cateinfo.catename
        data = gen_data(0,0,[])
        return render(request, "manager/category/move.html", locals())

    def post(self, request):
        CategoryModel.objects.filter(pk=request.GET.get("id")).update(
            followid = request.POST.get("followid")
        )
        result = {"state": "success", "msg": "保存成功"}
        return JsonResponse(result, safe=False)


def switchs(request):
    id = request.GET.get("id", 0)
    type = request.GET.get("type", 0)
    state = request.POST.get("state", 0)
    if type == '1':
        CategoryModel.objects.filter(cateid=id).update(isshow=state)
    if type == '2':
        CategoryModel.objects.filter(cateid=id).update(isblank=state)
    if type == '3':
        CategoryModel.objects.filter(cateid=id).update(isfilter=state)
    result = {"state": "success", "msg": "操作成功"}
    return JsonResponse(result, safe=False)


def delete(request):
    CategoryModel.objects.filter(pk=request.GET.get("id")).delete()
    result = {"state": "success", "msg": "删除成功"}
    return JsonResponse(result, safe=False)

def gen_data(pid=0, depth=0, res=[], astr=''):
    cateitems = CategoryModel.objects.filter(followid=pid)
    if cateitems:
        for cateitem in cateitems:
            item = dict(
                cateid = cateitem.cateid,
                catename = cateitem.catename,
                followid = cateitem.followid,
                depth = depth,
                astr = astr
            )
            res.append(item)
            if CategoryModel.objects.filter(followid=cateitem.cateid):
                tdepth = depth + 1
                bstr = astr + '&nbsp;&nbsp;&nbsp;&nbsp;'
                gen_data(cateitem.cateid, tdepth, res, bstr)
        return res


def refresh(request):
    cateitems = CategoryModel.objects.all()

    file_content = ""
    if cateitems:
        for cateitem in cateitems:
            parentid = get_parent(cateitem.cateid)
            sonid = get_sonid(cateitem.cateid)
            depth = get_depth(cateitem.cateid)
            serializers = CategorySerializers(cateitem)
            serializers.data.update(parentid=parentid, sonid=sonid, depth=depth)
            file_content += f"\nCATE_{cateitem.cateid} = {serializers.data}"
            CategoryModel.objects.filter(pk=cateitem.cateid).update(parentid=parentid, sonid=sonid, depth=depth)
    
    # 设置文件路径
    file_path = os.path.join(settings.BASE_DIR / 'conf', 'category_settings.py')

    # 尝试创建并写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)
        print("文件创建并写入成功。")
    except IOError as e:
        print(f"文件创建或写入失败: {e}")
    
    result = {"state": "success", "msg": "操作成功"}
    return JsonResponse(result, safe=False)
