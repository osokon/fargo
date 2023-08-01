from administration.slack_api import getAgents
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('users/', users, name='users'),
    path('roles/', roles, name='roles'),
    path('users/filter/', users_filter, name='users_filter'),
    path('users/export/', export_users, name='export_users'),
    path('user/activities/', user_activities, name='user_activities'),
    path('user/<int:id>/profile/', user_profile, name='user_profile'),
    path('add/user/', UserCreate.as_view(), name="add_user"),
    path('add/role/', GroupCreate.as_view(), name="add_group"),
    path('api/agents/list/', getAgents),
]
