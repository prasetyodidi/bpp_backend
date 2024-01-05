from django.urls import path

from chat import views

app_name = 'chat'
urlpatterns = [
    path('create-user-and-group', views.create_user_and_group, name='create_user_and_group'),
    path('create-user-and-join-group', views.create_user_and_join_group, name='create_user_and_join_group'),
    path('groups', views.user_groups, name='user_groups'),
    path('groups/join', views.join_group, name='user_join_group'),
    path('messages', views.add_message, name='user_add_message'),
    path('groups/<int:group_id>/change-time-period', views.change_time_period, name='user_change_group_time_period'),
    path('groups/<int:group_id>', views.messages_by_group_id, name='get_messages_by_group_id'),
]
