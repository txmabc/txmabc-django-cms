from django.urls import path

from home.views import index, news, product, page, job, book, other, search

app_name="home"
urlpatterns = [
    path("", index.index, name="index"),
    path("sitemap", other.sitemap, name="sitemap"),
    
    path('news/list/<int:classid>.html', news.lists, name="news_list"),
    path('news/show/<int:id>.html', news.show, name="news_show"),

    path('product/list/<int:classid>.html', product.lists, name="pro_list"),
    path('product/show/<int:id>.html', product.show, name="pro_show"),

    path('job/list/<int:classid>.html', job.lists, name="job_list"),
    path('job/show/<int:id>.html', job.show, name="job_show"),
    path('job/form/', job.FormView.as_view(), name="job_form"),

    path('page/<int:classid>.html', page.page, name="page_show"),

    path('book.html', book.IndexView.as_view(), name="book"),
    path('taglist/<int:id>.html', other.taglist, name="taglist"),
    path('tags.html', other.tags, name="tags"),

    path('search', search.IndexView.as_view(), name="search"),
    path('book.html', book.IndexView.as_view(), name="book"),
    path('tags', other.tags, name="tags"),
    path('taglist/<int:id>.html', other.taglist, name="taglist"),

    path('search', search.IndexView.as_view(), name="search"),
    
    path('other/ordershow/<int:orderid>', other.OrdershowView.as_view(), name="other_ordershow"),
    path('other/order', other.OrderView.as_view(), name="other_order"),
    path('other/inquiry', other.InquiryView.as_view(), name="other_inquiry"),
    path('other/orderpay/<int:orderid>', other.OrderPayView.as_view(), name="other_orderpay"),
]