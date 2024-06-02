from django.urls import path

from users.views import index, face, LoginView, RegisterView, PayView, LogoutView, UserInfoView, myorder, mymoney, GetpassView, EditpassView, EditemailView

app_name = 'users'
urlpatterns = [
    path("index", index, name="index"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("getpass", GetpassView.as_view(), name="getpass"),
    path("editemail", EditemailView.as_view(), name="editemail"),
    path("editpass", EditpassView.as_view(), name="editpass"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("userinfo", UserInfoView.as_view(), name="userinfo"),
    path("myorder", myorder, name="myorder"),
    path("mymoney", mymoney, name="mymoney"),
    path("pay", PayView.as_view(), name="pay"),
    path("face", face, name="face"),
]