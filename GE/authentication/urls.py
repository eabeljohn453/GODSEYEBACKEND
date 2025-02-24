from django.urls import path
from .views import login_view, admin_view, logout_view  # Import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', admin_view, name='admin_view'),  # Ensure this is correct
    path('logout/', logout_view, name='logout'),  # Logout route
]
