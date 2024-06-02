from django import forms
from captcha.fields import CaptchaField
from .models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'ui-form-ip'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'ui-form-ip radius-right-none'}))
    captcha = CaptchaField()