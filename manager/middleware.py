# Create your middleware here.
from django.shortcuts import redirect
from django.urls import reverse, resolve
# from manager.function import C
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # print(resolve(request.path))
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.get_full_path().startswith('/manager'):
            if not request.get_full_path().startswith('/manager/login'):
                if not request.session.get("adminid"):
                    return redirect(reverse('manager:login'))
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response