from django.urls import path
from .views import login_view, user_view, admin_view, logout_view, video_feed, admin_dashboard, dashboard_view, add_user, users_list, delete_user


urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', admin_view, name='admin_dashboard'),
    path('user/', user_view, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('video_feed/', video_feed, name='video_feed'),
    path('admin-dashboard/', dashboard_view, name='admin_dashboard'),
    path('add_user/', add_user, name='add_user'),  # Add user API
    path('users_list/', users_list, name='users_list'),  # Fetch users API
    path('delete_user/', delete_user, name='delete_user'),
]
