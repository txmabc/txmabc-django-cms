from manager.models import CategoryModel

def get_sonid(id:int)->str:
	subs=[]
	subs.append(id)
	no_subs = []
	while True:
		xlen = len(subs)
		items = CategoryModel.objects.filter(followid__in=subs).exclude(cateid__in=no_subs).all()
		for item in items:
			subs.append(item.cateid)
			no_subs.append(item.cateid)
		if not len(subs) > xlen:
			break
	if len(subs)>1:
		return ', '.join(str(t) for t in subs)
	return subs[0]


def get_parent(id:int)->str:
    subs = []
    while id:
        data = CategoryModel.objects.filter(cateid=id).get()
        subs.append(data.cateid)
        id= data.followid
    if len(subs)>1:
        return ', '.join(str(t) for t in subs)
    return subs[0]


def get_depth(id:int)->int:
    ids = str(get_parent(id))
    if ',' in ids:
        subs = ids.split(',')
        return len(subs)
    return 1

def get_catename(id:int)->str:
	data = CategoryModel.objects.get(pk=id)
	return data.catename

#系统资源
def C(a = None):
	global web_config
	if not a:
		return web_config
	if isinstance(a, str):
		if a.find('.') == -1:
			a = a.upper()
			return web_config[a] if web_config[a] else None
		else:
			a = a.split('.')
			a[0]=a[0].upper
			return web_config[a[0]][a[1]] if web_config[a[0]][a[1]] else None
	if isinstance(a, dict):
		for key,value in a.items():
			web_config.update({key.upper(), value})
		return None
	return None