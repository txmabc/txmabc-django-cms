from django.shortcuts import render

def is_mobile(request):
    user_agent = request.META['HTTP_USER_AGENT'].lower()
    mobile_keywords = ['Mobile', 'Android', 'iPad', 'iPod', 'BlackBerry']
    print(user_agent)
    for keyword in mobile_keywords:
        if keyword.lower() in user_agent:
            return True
            
    return False
 
# 在视图函数中使用
def my_render(request, temp_name, data):    
    if is_mobile(request):
        temp_prefix = 'home/mobile/'
        return render(request, temp_prefix + temp_name, data)
    else:
        temp_prefix = 'home/'
        return render(request, temp_prefix + temp_name, data)
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip