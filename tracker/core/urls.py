from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.dashboard, name='dashboard'),
    path('tasks/new/', views.task_create, name='task_create'),
]