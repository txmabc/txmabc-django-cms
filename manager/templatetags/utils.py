from django.template import Library
import re
from datetime import datetime
from manager.models import CategoryModel
from django.urls import reverse
from django import template
from django.db import connection
from PIL import Image
import os
from django.conf import settings
import math
import json
from manager.function import get_catename

register = Library()

# 生成缩略图
@register.simple_tag(name="thumb")
def thumb(file, width=200, height=200, type=1):
	if type==0:
		return file
	if not file:
		return ''
	if '://' in file:
		return file
	
	file_path = os.path.join(settings.MEDIA_URL, file)

	return file

	# 打开原始图片
	image = Image.open(file_path)
	
	# 设置缩略图大小（这里将其调整为200x200像素）
	thumbnail_size = (width, height)
	
	# 生成缩略图
	thumbnail = image.resize(thumbnail_size)
	
	# 获取原始图片路径及名称
	file_name, extension = os.path.splitext(os.path.basename(file))
	
	# 构造新的缩略图文件名
	new_file_name = f"{file_path}/thumb_{width}_{height}{extension}"
	
	# 保存缩略图到指定位置
	thumbnail.save(new_file_name)

	

@register.simple_tag(name="get_cate_info")
def get_cate_info(id, field, default=''):
	try:
		arr = CategoryModel.objects.filter(cateid=id).get()
		cate = arr.__dict__
		return cate[field]
	except CategoryModel.DoesNotExist:
		return default


@register.filter(name="get_cate_add_url")
def get_cate_add_url(classid, default="lists"):
	try:
		arr = CategoryModel.objects.filter(cateid=classid).get()
		if arr.catetype == 1:
			return f"/manager/news/add/?classid={classid}"
		if arr.catetype == 2:
			return f"/manager/product/add/?classid={classid}"
		if arr.catetype == 3:
			return f"/manager/job/add/?classid={classid}"

	except CategoryModel.DoesNotExist:
		return default

	
@register.filter(name="get_cate_edit_url")
def get_cate_edit_url(classid, id):
	try:
		arr = CategoryModel.objects.filter(cateid=classid).get()
		if arr.catetype == 1:
			return f"/manager/news/edit/?classid={classid}&id={id}"
		if arr.catetype == 2:
			return f"/manager/product/edit/?classid={classid}&id={id}"
		if arr.catetype == 3:
			return f"/manager/job/edit/?classid={classid}&id={id}"
	except CategoryModel.DoesNotExist:
		return ""


@register.filter(name="split")
def split(value, key):
	if key in value:
		return value.split(key)
	else:
		return [value]

@register.filter(name="strip")
def strip(value, key):
	"""
	Returns the value turned into a list.
	"""
	return value.strip(key)

@register.simple_tag(name="deal_rule")
def deal_rule(la,lb,lc=0):
	ld=''
	if la == '1': 
		ld='null'
	if la == '2': 
		ld='date'
	if la == '3': 
		ld='int'
	if la == '4': 
		ld='dot'
	if la == '5': 
		ld='tel'
	if la == '6': 
		ld='mobile'
	if la == '7': 
		ld='email'
	if la == '8': 
		ld='zipcode'
	if la == '9': 
		ld='qq'
	if la == '10': 
		ld='url'
	if la == '11': 
		ld='username'
	if la == '12': 
		ld='password'
	if la == '13': 
		ld='idcard'

	if ld=='':
		return ''
	else:
		ld=ld.replace('null','')
		if lc == 0:
			return 'data-rule="{lb}:required{ld}"'
		else:
			return 'data-rule="{lb}:checked{ld}"'

def findall(pattern, string):
	res = {}
	for match in re.finditer(pattern, string):
		res[match.group(0)] = match.start()
	return res

@register.simple_tag(name="deal_default")
def deal_default(sa):
	pat = re.compile(r'\{php:(.*?)}') #用()表示1个组，2个组
	m = pat.findall(sa)

	if m:
		for s in m:
			if s == 'now':
				return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	else:
		return sa
	
@register.filter(name='fromunix')
def fromunix(value, format='%Y-%m-%d %H:%I:%S'):
	return datetime.fromtimestamp(int(value)).strftime(format)

@register.filter(name='cateurl')
def cateurl(value):
	catetype = get_cate_info(value, 'catetype')
	if catetype == -1:
		value = f'/page/{value}.html'
	if catetype == 1:
		value = f'/news/list/{value}.html'
	if catetype == 2:
		value = f'/product/list/{value}.html'
	if catetype == 3:
		value = f'/job/list/{value}.html'
	return value

@register.simple_tag(name="get_cate_home_url")
def get_cate_home_url(cateid, catetype, cateurl):
	if catetype == -2:
		if cateurl.startswith('http'):
			return cateurl
		else:
			return '/' + cateurl + '.html'
	if catetype == -1:
		return f"/page/{cateid}.html"
	if catetype == 1:
		return f"/news/list/{cateid}.html"
	if catetype == 2:
		return f"/product/list/{cateid}.html"
	if catetype == 3:
		return f"/job/list/{cateid}.html"


@register.simple_tag(name="is_active")
def is_active(classid, pid=0, style=' class="hover"', type=0):
	if style != ' class="hover"':
		style = ' class="' + style + '"'
	if type == 1:
		style = style.replace("class=",'').replace("\"", '')
	if ',' in pid:
		parentid = [int(pid) for pid in pid.split(',')]
	else:
		parentid = [int(pid)]
	return style if classid in parentid else ''


@register.simple_tag(name="get_admin_menu_url")
def get_admin_menu_url(cname, aname, dname):
	return reverse('manager:'+cname + '_' + aname)


@register.tag(name='for_rp')
@register.tag(name='for_rs')
def do_custom_for(parser, token):
	tag_name = token.split_contents()[0]
	data = token.split_contents()[1:]
	args = {}
	for item in data:
		x,y = item.split('=', maxsplit=1)
		args[f'{x}']=y.strip('"')
	table = args['table']

	if 'key' in args.keys() and args['key']:	
		key = args["key"]
	else:
		key = 'id'
	
	if 'pagesize' in args.keys() and args['pagesize']:	
		pagesize = args["pagesize"]
	else:
		pagesize = 0

	if 'join' in args.keys() and args['join']:	
		join = args["join"]
	else:
		join = ''

	if 'where' in args.keys() and args['where']:
		where = f'where {args["where"]}'
	else:
		where = '1=1'
	
	if 'order' in args.keys() and args['order']:	
		order = f'order by {args["order"]}'
	else:
		order = ''

	if 'top' in args.keys() and args['top'] and args["top"] != '0':
		top = f'limit {args["top"]}'
	else:
		top = ''

	if 'field' in args.keys() and args['field']:	
		field = args["field"]
	else:
		field = '*'
	if tag_name == 'for_rp':
		nodelist = parser.parse(('endfor_rp',))
	if tag_name == 'for_rs':
		nodelist = parser.parse(('endfor_rs',))
	parser.delete_first_token()
	
	return CustomForNode(tag_name, table, field, top, join, where, order, key, pagesize, nodelist)
 

class CustomForNode(template.Node):
	def __init__(self, tag_name, table, field, top, join, where, order, key, pagesize, nodelist):
		self.join = join
		self.table = table
		self.field = field
		self.top = top
		self.where = where
		self.order = order
		self.nodelist = nodelist
		self.pagesize = pagesize
		self.key = key
		self.tag_name = tag_name
	
	def render(self, context):
		request = context['request']
		#获取总数量
		tsql = f"select count(1) from {self.table} {self.join} {self.where}"

		if '{{' in tsql:
			tsql = template.Template(tsql).render(context)

		with connection.cursor() as cursor:
				# 执行SQL语句并返回结果集
			cursor.execute(tsql)
			total_rs = cursor.fetchone()[0]
			context['request'].total_rs = total_rs

		if self.pagesize:
			#每页数量
			pagesize= int(self.pagesize)
			if pagesize<=0:
				pagesize=10

			#当前页数，默认第一页
			page=request.GET.get('page',1)
			totalpage = math.ceil(total_rs/pagesize)
			if page > totalpage:
				page=1
			offset = (page-1)*pagesize
			way = 0
			if offset>1000 and total_rs>2000 and offset>total_rs/2:
				offset = total_rs - offset - pagesize
				way = 1
			if offset < 0:
				pagesize += offset
				offset=0

			if way == 1:
				self.order = self.order.replace("desc","asc")

			key_sql=f"select id from {self.table} {self.join} {self.where} {self.order} limit {offset},{pagesize}"
			if '{{' in key_sql:
				key_sql = template.Template(key_sql).render(context)
			with connection.cursor() as cursor:
				# 执行SQL语句并返回结果集
				cursor.execute(key_sql)
				data_id = dictfetchall(cursor)
				
				if data_id:
					ids = ''
					for item in data_id:
						ids += str(item['id'])+','
					ids = ids.strip(',')
					self.where = f"where {self.key} in({ids})"

		sql = f"SELECT {self.field} FROM {self.table} {self.join} {self.where} {self.order} {self.top}"
		if '{{' in sql:
			sql = template.Template(sql).render(context)
		
		
		with connection.cursor() as cursor:
			cursor.execute(sql)
			rows = dictfetchall(cursor)
		output = []
		for row in rows:
			with context.push():
				if self.tag_name == 'for_rp':
					context['rp'] = row
				if self.tag_name == 'for_rs':
					context['rs'] = row
				output.append(self.nodelist.render(context))
		return ''.join(output)


def dictfetchall(cursor):
	# "Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]


@register.tag(name='get_sonid_all')
def do_get_sonid_all(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		tag_name, id = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires a single argument" % token.contents.split()[0]
		)
	# if not (id[0] == id[-1] and id[0] in ('"', "'")):
	# 	raise template.TemplateSyntaxError(
	# 		"%r tag's argument should be in quotes" % tag_name
	# 	)

	subs=[]
	subs.append(int(id))
	no_subs = []
	while True:
		xlen = len(subs)
		items = CategoryModel.objects.filter(followid__in=subs).exclude(cateid__in=no_subs).all()
		for item in items:
			subs.append(item.cateid)
			no_subs.append(item.cateid)
		if not len(subs) > xlen:
			break
	return CurrentSonidNode(subs)

class CurrentSonidNode(template.Node):
	def __init__(self, subs):
		self.subs = subs
	def render(self, context):
		self.subs = list(map(str, self.subs))
		context['subs'] = ','.join(self.subs)
		return ''
	
@register.filter(name='json_decode')
def json_decode(value):
	return json.loads(value)


@register.filter(name='get_catename')
def get_cateinfo_catename(value):
	return get_catename(int(value))