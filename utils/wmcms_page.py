import copy

class WmcmsPage():
    def __init__(self, request, totalnum, totalpage, pagesize, thispage):
        self.totalnum = totalnum
        self.totalpage = totalpage
        self.pagesize = pagesize
        self.thispage = thispage
        self.req = copy.deepcopy(request.GET)#深拷贝get请求
        self.req._mutable = True
        self.config = {
            'total' : '总数：',
            'home'  : '首页',
            'pre'   : '上一页',
            'next'  : '下一页',
            'last'  : '末页',
        }
        if self.totalnum==0:
            self.totalpage=0
        if self.totalpage==0:
            self.thispage=1
        if self.thispage>self.totalpage:
            self.thispage=1
            
    def getUrl(self,num):
        self.req.setlist('page', f'{num}')#iter必须是可迭代对象
        mstr = '?' + self.req.urlencode()
        return mstr

        
    def pageList(self,j=5):
        if self.totalpage==1:
            return ''
        i=j
        begin=self.thispage
        end=self.thispage; 
        while True:
            if begin>1:
                begin = begin-1
                i = i-1
            if i > 1 and end < self.totalpage:
                end = end + 1
                i=i-1
            if (begin<=1 and end>=self.totalpage) or i<=1:
                break
        str=''
        str += f'<li><a>{self.config["total"]}{self.totalnum}</a></li>'
        
        if self.thispage>1:
            str += f'<li><a href="{self.getUrl(self.thispage-1)}">{self.config["pre"]}</a></li>'
        if begin!=1:
            str += f'<li><a href="{self.getUrl(1)}">1...</a></li>'

        for i in range(begin, end):
            if i==self.thispage:
                str += f'<li class="active"><a href="{self.getUrl(i)}">{self.thispage}</a></li>'
            else:
                str += f'<li><a href="{self.getUrl(i)}">{i}</a></li>'

        if end!=self.totalpage:
            str += f'<li><a href="{self.getUrl(self.totalpage)}">...{self.totalpage}</a></li>'
        if self.thispage<self.totalpage:
            str += f'<li><a href="{self.getUrl(self.thispage+1)}">{self.config["next"]}</a></li>'

        str += f'<li><a>{self.thispage}/{self.totalpage}</a></li>'
        return str
    
    #组合
    def showpage(self,a):
        if self.totalpage==0:
            return ''
        return self.pageList(a)