from django.urls import path
from .views import login_view, user_view, admin_view, logout_view  # Import views
from .views import video_feed, admin_dashboard
from .views import dashboard_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', admin_view, name='admin_dashboard'),  # Keep only one reference for the admin dashboard
    path('user/', user_view, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('video_feed/', video_feed, name='video_feed'),
    path('admin-dashboard/', dashboard_view, name='admin_dashboard'),
]