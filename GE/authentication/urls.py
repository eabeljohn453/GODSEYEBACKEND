# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/', views.admin_view, name='admin'),
    path('user/', views.user_view, name='user')  # Ensure this is correctly set
]
