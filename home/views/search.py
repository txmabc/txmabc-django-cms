from django.shortcuts import render
from django.views import View


# 添加内容
class IndexView(View):
    def get(self, request):
        catename = "站内搜索"
        encatename = "Search"

        return render(request, "home/search.html",locals())

    def post(self, request):
        keyword = request.POST.get("keyword", None)
        return render(request, "home/search.html",locals())