from django.urls import path

from chat import views

app_name = 'chat'
urlpatterns = [
    path('create-user-and-group', views.create_user_and_group, name='create_user_and_group')
]
