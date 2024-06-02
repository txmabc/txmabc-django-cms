from django.urls import path

from manager.views import index, login, order, mail, inquiry, tags, admin, config, configgroup, configgroupfield, menu, part, plugservice, category, content, user, usergroup, usermoney, advert, book, block, upload, news, product, job, resume, link

app_name="manager"
urlpatterns = [
    path("", index.index, name="index"),
    path("right/", index.right, name="right"),
    path("login/", login.IndexView.as_view(), name="login"),
    path("out/", index.out, name="out"),

    path("index/pass", index.PassView.as_view(), name="index_pass"),

    path("admin/index", admin.IndexView.as_view(), name="admin_index"),
    path("admin/edit?id=<int:id>", admin.EditView.as_view(), name="admin_edit"),
    path("admin/add", admin.AddView.as_view(), name="admin_add"),
    path("admin/switchs?type=<int:type>&id=<int:id>", admin.switchs, name="admin_switchs"),
    path("admin/del?id=<int:id>", admin.delete, name="admin_del"),

    path("usergroup/index", usergroup.IndexView.as_view(), name="usergroup_index"),
    path("usergroup/edit?id=<int:id>", usergroup.EditView.as_view(), name="usergroup_edit"),
    path("usergroup/add", usergroup.AddView.as_view(), name="usergroup_add"),
    path("usergroup/del?id=<int:id>", usergroup.delete, name="usergroup_del"),

    path("config/index/", config.IndexView.as_view(), name="config_index"),
    path("config/index/<int:id>/", config.IndexView.as_view(), name="config_index"),

    path("book/index/", book.IndexView.as_view(), name="book_index"),
    path("book/edit?id=<int:id>", book.EditView.as_view(), name="book_edit"),
    path("book/del/", book.delete, name="book_del"),

    path("part/index/", part.IndexView.as_view(), name="part_index"),
    path("part/add/", part.AddView.as_view(), name="part_add"),
    path("part/edit?id=<int:id>", part.EditView.as_view(), name="part_edit"),
    path("part/page?id=<int:id>", part.PageView.as_view(), name="part_page"),
    path("part/cate?id=<int:id>", part.CateView.as_view(), name="part_cate"),
    path("part/del?id=<int:id>", part.delete, name="part_del"),

    path("menu/index/", menu.IndexView.as_view(), name="menu_index"),
    path("menu/index?fid=<int:fid>", menu.IndexView.as_view(), name="menu_index"),
    path("menu/add?fid=<int:fid>", menu.AddView.as_view(), name="menu_add"),
    path("menu/edit?id=<int:id>", menu.EditView.as_view(), name="menu_edit"),
    path("menu/switchs?id=<int:id>", menu.switchs, name="menu_switchs"),
    path("menu/del?id=<int:id>", menu.delete, name="menu_del"),

    path("advert/index/", advert.IndexView.as_view(), name="advert_index"),
    path("advert/add/", advert.AddView.as_view(), name="advert_add"),
    path("advert/edit/<int:id>.html", advert.EditView.as_view(), name="advert_edit"),
    path("advert/switchs/", advert.switchs, name="advert_switchs"),

    path("link/index/", link.IndexView.as_view(), name="link_index"),
    path("link/add/", link.AddView.as_view(), name="link_add"),
    path("link/edit/<int:id>.html", link.EditView.as_view(), name="link_edit"),
    path("link/config/", link.ConfigView.as_view(), name="link_config"),
    path("link/config?id=<int:id>", link.ConfigView.as_view(), name="link_config"),
    path("link/switchs?id=<int:id>", link.switchs, name="link_switchs"),
    path("link/del?id=<int:id>", link.delete, name="link_del"),

    path("category/index/", category.IndexView.as_view(), name="category_index"),
    path("category/index?fid=<int:fid>", category.IndexView.as_view(), name="category_index"),
    path("category/add/", category.AddView.as_view(), name="category_add"),
    path("category/edit/", category.EditView.as_view(), name="category_edit"),
    path("category/move/", category.MoveView.as_view(), name="category_move"),
    path("category/del/", category.delete, name="category_del"),
    path("category/switchs/", category.switchs, name="category_switchs"),
    path("category/refresh/", category.refresh, name="category_refresh"),
    
    path("content/index/", content.IndexView.as_view(), name="content_index"),
    path("content/page/", content.PageView.as_view(), name="content_page"),
    path("content/recycle/", content.recycle, name="content_recycle"),
    path("content/lists/", content.lists, name="content_lists"),
    path("content/taglist/", content.taglist, name="content_taglist"),
    path("content/delete/", content.delete, name="content_delete"),
    path("content/clear/", content.clear, name="content_clear"),
    path("content/btach/", content.btach, name="content_btach"),
    path("content/switchs/", content.switchs, name="content_switchs"),
    path("content/tree/", content.tree, name="content_tree"),
    path("content/move/", content.move, name="content_move"),

    path("user/index/", user.IndexView.as_view(), name="user_index"),
    path("user/index?uid=<int:uid>", user.IndexView.as_view(), name="user_index"),
    path("user/index?type=<int:type>", user.IndexView.as_view(), name="user_index"),
    path("user/add/", user.AddView.as_view(), name="user_add"),
    path("user/edit?id=<int:id>", user.EditView.as_view(), name="user_edit"),
    path("user/switchs?id=<int:id>", user.switchs, name="user_switchs"),
    path("user/gouser?id=<int:id>", user.gouser, name="user_gouser"),
    path("user/clear?id=<int:id>", user.clear, name="user_clear"),
    path("user/del?id=<int:id>", user.delete, name="user_del"),

    path("news/add/", news.AddView.as_view(), name="news_add"),
    path("news/edit/", news.EditView.as_view(), name="news_edit"),

    path("product/add/", product.AddView.as_view(), name="product_add"),
    path("product/edit/", product.EditView.as_view(), name="product_edit"),

    path("job/add/", job.AddView.as_view(), name="job_add"),
    path("job/edit/", job.EditView.as_view(), name="job_edit"),

    path("resume/index/", resume.IndexView.as_view(), name="resume_index"),
    path("resume/add/", resume.AddView.as_view(), name="resume_add"),
    path("resume/edit/", resume.EditView.as_view(), name="resume_edit"),
    path("resume/switchs/", resume.switchs, name="resume_switchs"),

    path("configgroup/index/", configgroup.IndexView.as_view(), name="configgroup_index"),
    path("configgroup/add/", configgroup.AddView.as_view(), name="configgroup_add"),
    path("configgroup/edit?id=<int:id>", configgroup.EditView.as_view(), name="configgroup_edit"),
    path("configgroup/switchs?id=<int:id>", configgroup.switchs, name="configgroup_switchs"),
    path("configgroup/del?id=<int:id>", configgroup.delete, name="configgroup_del"),

    path("configgroupfield/index?gid=<int:gid>", configgroupfield.IndexView.as_view(), name="configgroupfield_index"),
    path("configgroupfield/add?gid=<int:gid>", configgroupfield.AddView.as_view(), name="configgroupfield_add"),
    path("configgroupfield/edit?id=<int:id>", configgroupfield.EditView.as_view(), name="configgroupfield_edit"),
    path("configgroupfield/switchs?id=<int:id>", configgroupfield.switchs, name="configgroupfield_switchs"),
    path("configgroupfield/del?id=<int:id>", configgroupfield.delete, name="configgroupfield_del"),

    path("block/index/", block.index, name="block_index"),
    path("block/add/", block.AddView.as_view(), name="block_add"),
    path("block/edit/", block.EditView.as_view(), name="block_edit"),
    path("block/del?id=<int:id>", block.delete, name="block_del"),

    path("upload/imageupload?type=<int:type>&multiple=<int:multiple>", upload.imageupload, name="upload_imageupload"),
    path("upload/imagelist?type=<int:type>&multiple=<int:multiple>", upload.imagelist, name="upload_imagelist"),

    path("upload/imageupload/", upload.imageupload, {'type':1,'multiple':0}, name="imageupload"),
    path("upload/imagelist/", upload.imagelist, name="imagelist"),
    path("upload/uploadfile", upload.uploadfile, name="uploadfile"),
    path("upload/upload_tinymce/", upload.upload_tinymce, name="upload_tinymce"),
    path("upload/upload_editor/", upload.upload_editor, name="upload_editor"),

    path("plug/service/index/", plugservice.IndexView.as_view(), name="plugservice_index"),
    path("plug/service/add/", plugservice.AddView.as_view(), name="plugservice_add"),
    path("plug/service/edit?id=<int:id>", plugservice.EditView.as_view(), name="plugservice_edit"),
    path("plug/service/del?id=<int:id>", plugservice.delete, name="plugservice_del"),

    path("tags/index/", tags.index, name="tags_index"),
    path("tags/clear/", tags.clear, name="tags_clear"),
    path("tags/delete?id=<int:id>", tags.delete, name="tags_del"),

    path("order/index/", order.index, name="order_index"),
    path("order/edit?id=<int:id>", order.EditView.as_view(), name="order_edit"),
    path("order/btach/", order.btach, name="order_btach"),
    path("order/del?id=<int:id>", order.delete, name="order_del"),
    path("order/switchs/", order.switchs, name="order_switchs"),

    path("user/money/index/", usermoney.index, name="usermoney_index"),
    path("user/money/add/", usermoney.AddView.as_view(), name="usermoney_add"),
    path("user/money/del?id=<int:id>", usermoney.delete, name="usermoney_del"),

    path("inquiry/index/", inquiry.index, name="inquiry_index"),
    path("inquiry/edit?id=<int:id>", inquiry.EditView.as_view(), name="inquiry_edit"),
    path("inquiry/del?id=<int:id>", inquiry.delete, name="inquiry_del"),
    path("inquiry/switchs/", inquiry.switchs, name="inquiry_switchs"),
    path("inquiry/btach/", inquiry.btach, name="inquiry_btach"),

    path("mail/index/", mail.index, name="mail_index"),
    path("mail/edit?id=<int:id>", mail.EditView.as_view(), name="mail_edit"),
    path("mail/add/", mail.AddView.as_view(), name="mail_add"),
    path("mail/del?id=<int:id>", mail.delete, name="mail_del"),
    path("mail/switchs?id=<int:id>", mail.switchs, name="mail_switchs"),
]