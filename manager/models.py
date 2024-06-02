from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    adminname = models.CharField(max_length=50, verbose_name="用户名", unique=True, null=True)
    adminpass = models.CharField(max_length=256, verbose_name="密码", null=True)
    penname = models.CharField(max_length=20, verbose_name="昵称", null=True)
    pid = models.IntegerField(default=0, verbose_name="部门")
    logintimes = models.IntegerField(default=0, verbose_name="登录次数")
    lastlogindate = models.DateTimeField(null=True, blank=True, verbose_name="最后登录日期")
    lastloginip = models.GenericIPAddressField(null=True, verbose_name="上次登录IP")
    islock = models.IntegerField(default=0, verbose_name="状态")
    readonly = models.SmallIntegerField(default=0, verbose_name="是否只读")

    def __str__(self):
        return self.adminname


class AdminLog(models.Model):
    title = models.CharField(max_length=50, verbose_name="用户名", null=True)
    url = models.CharField(max_length=255, verbose_name="密码", null=True)
    msg = models.CharField(max_length=255, verbose_name="消息", null=True)
    ip = models.CharField(max_length=50, verbose_name="IP", null=True)
    createdate = models.DateTimeField(auto_now_add=True, verbose_name="日期")

    def __str__(self):
        return self.title


class AdminLoginLog(models.Model):
    loginname = models.CharField(max_length=50, verbose_name="用户名", null=True)
    loginip = models.CharField(max_length=50, verbose_name="IP", null=True)
    logindate = models.DateTimeField(auto_now_add=True, verbose_name="日期")
    loginmsg = models.CharField(max_length=255, verbose_name="消息", null=True)
    loginstate = models.SmallIntegerField(verbose_name="状态", null=True)

    def __str__(self):
        return self.loginname


class AdminMenu(models.Model):
    title = models.CharField(max_length=50, verbose_name="菜单名称", null=True)
    cname = models.CharField(max_length=50, verbose_name="控制器名称", null=True)
    aname = models.CharField(max_length=50, verbose_name="动作名称", null=True)
    dname = models.CharField(max_length=255, verbose_name="附加参数", null=True)
    followid = models.IntegerField(default=0, verbose_name="父级")
    ordnum = models.IntegerField(default=0, verbose_name="菜单排序")
    islock = models.IntegerField(default=0, verbose_name="状态")

    def __str__(self):
        return self.title


class AdminPart(models.Model):
    title = models.CharField(max_length=50, verbose_name="部门名称", null=True)
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    page_list = models.TextField(verbose_name="页面权限")
    cate_list = models.TextField(verbose_name="栏目权限")
    pagelever = models.CharField(max_length=50, verbose_name="权限设置", null=True)
    pagelock = models.SmallIntegerField(verbose_name="审核设置", default=0)

    def __str__(self):
        return self.title


class AttachmentGroup(models.Model):
    aid = models.AutoField(primary_key=True)
    gname = models.CharField(max_length=50, verbose_name="部门名称", null=True)
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    islock = models.IntegerField(default=0, verbose_name="状态")

    def __str__(self):
        return self.gname


class Attachment(models.Model):
    file_url = models.CharField(max_length=255, verbose_name="url地址", null=True)
    file_name = models.CharField(max_length=255, verbose_name="文件名", null=True)
    file_ext = models.CharField(max_length=50, verbose_name="文件后缀", null=True)
    file_size = models.IntegerField(default=0, verbose_name="文件大小")
    file_type = models.IntegerField(default=0, verbose_name="文件类型", help_text="1：图片，2：视频，3：其他")
    file_update = models.DateTimeField(auto_now_add=True, verbose_name="上传的日期")
    file_local = models.IntegerField(default=0, verbose_name="存放位置", help_text="1：本地，2：阿里云，3：七牛云")
    file_adminid = models.IntegerField(default=0, verbose_name="管理员id")
    file_userid = models.IntegerField(default=0, verbose_name="用户id")
    file_ip = models.CharField(max_length=50, verbose_name="上传者IP", null=True)
    gid = models.IntegerField(default=0, verbose_name="分组")

    def __str__(self):
        return self.file_name


class CategoryModel(models.Model):
    cateid = models.AutoField(primary_key=True)
    catename = models.CharField(max_length=30, verbose_name="栏目名称")
    followid = models.IntegerField(default=0, verbose_name="父ID")
    depth = models.IntegerField(default = 1, verbose_name = "深度")
    sonid = models.TextField(null=True, verbose_name="所有子ID")
    parentid = models.TextField(null=True, verbose_name="所有父ID")
    catetype = models.IntegerField(default=0, verbose_name="栏目类型", help_text="-2：链接，-1：单页，1：文章，2：产品，3：招聘")
    catenum = models.IntegerField(default=0, verbose_name="排序", help_text="数字越小越靠前")
    cateurl = models.CharField(null=True, blank=True, max_length=255, verbose_name="链接")
    catepage = models.IntegerField(default=0, verbose_name="分页数量")
    categroup = models.CharField(null=True, blank=True, max_length=255, verbose_name="阅读权限")
    catelist = models.CharField(null=True, blank=True, max_length=255, verbose_name="列表页模板")
    cateshow = models.CharField(null=True, blank=True, max_length=255, verbose_name="内容页模板")
    catetitle = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO标题")
    catekey = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO关键字")
    catedesc = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO描述")
    isshow = models.IntegerField(default=0, verbose_name="导航显示")
    isblank = models.IntegerField(default=0, verbose_name="新窗口")
    isfilter = models.IntegerField(default=0, verbose_name="列表筛选")
    
    
    def __str__(self):
        return self.catename


class ContentModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="标题", null=True)
    pic = models.CharField(max_length=255, verbose_name="缩略图", null=True)
    ispic = models.IntegerField(default=0, verbose_name="图片")
    classid = models.IntegerField(default=0, verbose_name="分类")
    hits = models.IntegerField(default=0, verbose_name="人气")
    islock = models.IntegerField(default=0, verbose_name="状态")
    ontop = models.IntegerField(default=0, verbose_name="置顶")
    isnice = models.IntegerField(default=0, verbose_name="推荐")
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    upnum = models.IntegerField(default=0, verbose_name="赞数量")
    downnum = models.IntegerField(default=0, verbose_name="踩数量")
    isurl = models.IntegerField(default=0, verbose_name="链接")
    url = models.CharField(max_length=255, verbose_name="链接地址", null=True)
    createdate = models.IntegerField(default=0, verbose_name="创建时间")
    lastupdate = models.IntegerField(default=0, verbose_name="更新时间")
    intro = models.TextField(verbose_name="摘要")
    tags = models.CharField(max_length=255, verbose_name="标签", null=True)
    seotitle = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO标题")
    seokey = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO关键字")
    seodesc = models.CharField(null=True, blank=True, max_length=255, verbose_name="SEO描述")
    alias = models.CharField(null=True, blank=True, max_length=255, verbose_name="别名")
    showskin = models.CharField(null=True, blank=True, max_length=255, verbose_name="内容页模板")
    subid = models.CharField(max_length=255, verbose_name="发布到其它栏目", null=True)
    adminid = models.IntegerField(default=0, verbose_name="管理员")
    isauto = models.IntegerField(default=0, verbose_name="定时发布")
    view_groupid = models.CharField(max_length=50, null=True, blank=True, verbose_name="阅读权限")
    tagslist = models.CharField(null=True, blank=True, max_length=500, verbose_name="标签列表")

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['id', 'ontop', 'ordnum', 'classid', 'islock'], name='order'),
            models.Index(fields=['id', 'ontop'], name='ontop'),
            models.Index(fields=['id', 'ordnum'], name='ordnum'),
            models.Index(fields=['islock', 'classid', 'id', 'subid'], name='where'),
            models.Index(fields=['subid'], name='subid'),
            models.Index(fields=['islock', 'isauto', 'createdate'], name='isauto'),
        ]


class ModelNewsModel(models.Model):
    newsid = models.AutoField(primary_key=True)
    cid = models.IntegerField(default=0, verbose_name="cid", unique=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name="价格")
    content = models.TextField(verbose_name="正文")


class ModelProModel(models.Model):
    proid = models.AutoField(primary_key=True)
    cid = models.IntegerField(default=0, verbose_name="cid", unique=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name="价格")
    content = models.TextField(verbose_name="正文")
    piclist = models.TextField(verbose_name="组图")


class ModelJobModel(models.Model):
    jobid = models.AutoField(primary_key=True)
    cid = models.IntegerField(default=0, verbose_name="cid", unique=True)
    content = models.TextField(verbose_name="工作内容")
    work_address = models.CharField(max_length=50, verbose_name="工作地点", null=True)
    work_nature = models.CharField(max_length=50, verbose_name="工作性质", null=True)
    work_education = models.CharField(max_length=50, verbose_name="学历要求", null=True)
    work_money = models.CharField(max_length=50, verbose_name="薪资待遇", null=True)
    work_age = models.CharField(max_length=50, verbose_name="工作年限", null=True)
    work_num = models.CharField(max_length=50, verbose_name="招聘人数", null=True)


class ModelPageModel(models.Model):
    pageid = models.AutoField(primary_key=True)
    cid = models.IntegerField(default=0, verbose_name="cid", unique=True)
    piclist = models.TextField(verbose_name="图片集")
    content = models.TextField(verbose_name="正文")


class UserGroupModel(models.Model):
    gid = models.AutoField(primary_key=True)
    gname = models.CharField(max_length=30, verbose_name="分组名称")
    ordnum = models.IntegerField(default=0, verbose_name="排序", help_text="数字越小越靠前")

    def __str__(self):
        return self.gname


class ModelModel(models.Model):
    title = models.CharField(max_length=50, verbose_name="模型名称")
    tablename = models.CharField(max_length=50, verbose_name="模型标识")
    model_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="模型描述")
    list_skins = models.CharField(max_length=255, blank=True, null=True, verbose_name="列表模板")
    show_skins = models.CharField(max_length=255, blank=True, null=True, verbose_name="内容模板")
    form_group = models.CharField(max_length=255, blank=True, null=True, verbose_name="表单分组")
    ordnum = models.IntegerField(default=0, verbose_name="模型排序")
    islock = models.IntegerField(default=0, verbose_name="状态")
    leverstate = models.SmallIntegerField(default=0, verbose_name="阅读权限")
    buystate = models.SmallIntegerField(default=0, verbose_name="收费阅读")

    def __str__(self):
        return self.title


class TagsModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="标题", null=True)
    hits = models.IntegerField(default=0, verbose_name="热度")

    def __str__(self):
        return self.title


class BlockModel(BaseModel):
    title = models.CharField(max_length=50, verbose_name="区块说明")
    key = models.CharField(max_length=50, verbose_name="关键字")
    content = models.CharField(max_length=255, blank=True, null=True, verbose_name="内容")

    def __str__(self):
        return self.title


class AdvertModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="广告名称")
    datalist = models.TextField(verbose_name="广告内容")
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    islock = models.IntegerField(default=0, verbose_name="状态")
    akey = models.CharField(max_length=10, verbose_name="关键字")

    def __str__(self):
        return self.title


class JobFormModel(BaseModel):
    id = models.AutoField(primary_key=True)
    my_title = models.CharField(max_length=50, verbose_name="申请职位")
    my_truename = models.CharField(max_length=50, verbose_name="姓名")
    my_sex = models.IntegerField(default=0, verbose_name="性别")
    my_age = models.IntegerField(default=0, verbose_name="年龄")
    my_mobile = models.IntegerField(default=0, verbose_name="手机")
    my_education = models.IntegerField(default=0, verbose_name="学历")
    my_work_exp= models.TextField(verbose_name="工作经验")
    my_intro= models.TextField(verbose_name="自我评价")
    my_ip = models.CharField(max_length=50, blank=True, null=True, verbose_name="发布IP")
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    islock = models.IntegerField(default=0, verbose_name="状态")

    def __str__(self):
        return self.my_title


class BookModel(BaseModel):
    id = models.AutoField(primary_key=True)
    truename = models.CharField(max_length=50, verbose_name="姓名")
    tel = models.CharField(max_length=20, verbose_name="座机")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    remark= models.TextField(verbose_name="留言")
    reply= models.TextField(verbose_name="回复")
    islock = models.IntegerField(default=0, verbose_name="状态")
    ontop = models.IntegerField(default=0, verbose_name="置顶")
    createdate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    postip = models.CharField(max_length=20, verbose_name="座机")
    replydate = models.DateTimeField(default=timezone.now, verbose_name="回复时间")

    def __str__(self):
        return self.truename


class LinkModel(BaseModel):
    id = models.AutoField(primary_key=True)
    webname = models.CharField(max_length=50, verbose_name="网站名称")
    weblogo = models.CharField(max_length=255, verbose_name="网站LOGO")
    weburl = models.CharField(max_length=255, verbose_name="网址")
    islogo = models.IntegerField(default=0, verbose_name="islogo")
    classid = models.IntegerField(default=0, verbose_name="类别")
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    islock = models.IntegerField(default=0, verbose_name="状态")

    def __str__(self):
        return self.webname


class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=50, verbose_name="用户名")
    upass = models.TextField(max_length=256, verbose_name="密码")
    umoney = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name="余额")
    uemail = models.CharField(blank=True, null=True, max_length=50, verbose_name="邮箱")
    uface = models.CharField(blank=True, null=True, max_length=255, verbose_name="头像")
    uid = models.IntegerField(default=0, verbose_name="会员组")
    islock = models.IntegerField(default=0, verbose_name="状态")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="注册日期")
    regip = models.CharField(blank=True, null=True, max_length=50, verbose_name="注册IP")
    lastlogindate = models.DateTimeField(blank=True, null=True, verbose_name="上次登录日期")
    lastloginip = models.CharField(blank=True, null=True, max_length=50, verbose_name="上次登录IP")
    logintimes = models.IntegerField(default=0, verbose_name="登录次数")

    def __str__(self):
        return self.uname


class ConfigModel(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.IntegerField(default=0, verbose_name="分组")
    ckey = models.CharField(max_length=50, verbose_name="字段Key")
    ctitle = models.CharField(max_length=50, verbose_name="字段名称")
    cvalue = models.TextField(verbose_name="字段值")
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    ctype = models.IntegerField(default=0, verbose_name="字段类型")
    dvalue = models.TextField(verbose_name="字段默认值")
    dtext = models.CharField(max_length=255, verbose_name="提示文字")
    utype = models.IntegerField(default=0, verbose_name="上传类型")
    rtype = models.IntegerField(default=0, verbose_name="排列方式")
    issys = models.IntegerField(default=0, verbose_name="系统自带")
    islock = models.IntegerField(default=0, verbose_name="状态")
    ishide = models.IntegerField(default=0, verbose_name="是否隐藏")

    def __str__(self):
        return self.ctitle
    
    class Meta:
        indexes = [
            models.Index(fields=['ckey'], name='ckey'),
            models.Index(fields=['gid'], name='gid'),
        ]


class ConfigGroupModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="分组ID")
    gname = models.CharField(max_length=50, verbose_name="分组名称", null=True)
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    gkey = models.CharField(max_length=50, verbose_name="分组Key")
    islock = models.IntegerField(default=0, verbose_name="状态")
    types = models.IntegerField(default=0, verbose_name="分类")

    def __str__(self):
        return self.gname


class PlugService(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=50, verbose_name="客服名称", null=True)
    qq = models.CharField(max_length=50, verbose_name="QQ号码", null=True)
    ordnum = models.IntegerField(default=0, verbose_name="排序")
    islock = models.IntegerField(default=0, verbose_name="状态")

    def __str__(self):
        return self.title


class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    orderid = models.CharField(max_length=50, verbose_name="订单号", null=True)
    pro_name = models.CharField(max_length=255, verbose_name="产品名称", null=True)
    pro_num = models.IntegerField(default=0, verbose_name="数量")
    pro_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="总金额")
    truename = models.CharField(max_length=50, verbose_name="姓名", null=True)
    mobile = models.CharField(max_length=20, verbose_name="手机", null=True)
    address = models.CharField(max_length=255, verbose_name="收货地址", null=True)
    remark = models.TextField(verbose_name="备注", null=True)
    createdate = models.IntegerField(default=0, verbose_name="下单日期")
    isover = models.IntegerField(default=0, verbose_name="状态")
    ispay = models.IntegerField(default=0, verbose_name="付款状态")
    payway = models.CharField(max_length=50, verbose_name="付款方式", null=True)
    trade_no = models.CharField(max_length=255, verbose_name="交易号", null=True)
    postip = models.CharField(max_length=50, verbose_name="IP地址", null=True)
    userid = models.IntegerField(default=0, verbose_name="用户ID")

    def __str__(self):
            return self.pro_name

class UserMoney(models.Model):
    aid = models.AutoField(primary_key=True, verbose_name="ID")
    types = models.SmallIntegerField(default=0, verbose_name="性质")
    title = models.CharField(max_length=255, verbose_name="名称|流水号", null=True)
    userid = models.IntegerField(default=0, verbose_name="用户ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="金额")
    oldmoney = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="变动前")
    newmoney = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="变动后")
    createdate = models.IntegerField(default=0, verbose_name="日期")

    def __str__(self):
            return self.title

    
class Inquiry(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=255, verbose_name="询价产品", null=True)
    truename = models.CharField(max_length=50, verbose_name="姓名", null=True)
    mobile = models.CharField(max_length=20, verbose_name="手机", null=True)
    remark = models.TextField(verbose_name="备注", null=True)
    createdate = models.IntegerField(default=0, verbose_name="提交日期")
    isover = models.IntegerField(default=0, verbose_name="状态")
    postip = models.CharField(max_length=50, verbose_name="IP地址", null=True)

    def __str__(self):
            return self.title
    

class TempMail(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=255, verbose_name="用途", null=True)
    mail_title = models.CharField(max_length=255, verbose_name="邮件标题", null=True)
    mail_content = models.TextField(verbose_name="邮件内容", null=True)
    islock = models.IntegerField(default=0, verbose_name="状态")
    mkey = models.CharField(max_length=50, verbose_name="Key", null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id'),
            models.Index(fields=['mkey'], name='mkey'),
        ]