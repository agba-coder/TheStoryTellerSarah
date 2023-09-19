from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'login/$', views.login, name="login"),
    path('signup', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('favicon.ico', lambda _ : redirect('static/images/favicon.ico', permanent=True)),
]