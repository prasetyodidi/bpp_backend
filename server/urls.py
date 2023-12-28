from django.urls import re_path, include

from . import views

urlpatterns = [
    re_path('chat/', include("chat.urls")),
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('test_token', views.test_token),
]
