from django.urls import path
from user import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/', views.ListCreateUserView.as_view()),
    path('user/<int:pk>', views.UpdateDeleteUserView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create-user/', views.CreateUserView.as_view(), name = "create_user"),
    path('login/', views.LoginView.as_view(), name = "login"),
    path('logout/', views.LogoutView.as_view(), name = "logout")
]