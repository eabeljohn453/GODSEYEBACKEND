from django.urls import path
from .views import login_view,user_view, admin_view, logout_view  # Import views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', admin_view, name='admin_dashboard'),
    path('user/', user_view, name='user_dashboard'),  # This is the missing page
    path('logout/', logout_view, name='logout'),
]
