from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/profile/', views.dashboard, name='profile'),
    path('reminders/', views.reminder_create, name='reminder_create'),
]