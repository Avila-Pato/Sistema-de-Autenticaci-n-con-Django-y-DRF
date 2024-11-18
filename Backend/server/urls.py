from django.urls import path
from .views import login, register, profile, verify_email, create_password, generate_winner
from server import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/login/', login, name='login'),
    path('api/register/', register, name='register'),
    path('api/profile/', profile, name='profile'),
    path('api/verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('api/create-password/', create_password, name='create_password'),
    path('api/generate-winner/', generate_winner, name='generate_winner'),
    path('api/users/', views.get_all_users, name='get_all_users'),


     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
