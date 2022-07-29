from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
# from django.urls import include, url

app_name = "accountUser"
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/signin.html'), name="signin"),
    path('logout/', LogoutView.as_view(template_name='registration/signout.html'), name="logout"),

]
