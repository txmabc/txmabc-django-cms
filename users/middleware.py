# Create your middleware here.
from django.shortcuts import redirect
from django.urls import reverse, resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # print(resolve(request.path))
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.get_full_path().startswith('/users'):
            if not request.get_full_path().startswith('/users/login') and not request.get_full_path().startswith('/users/register'):
                if not request.session.get("user_info"):
                    return redirect(reverse('users:login'))
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response