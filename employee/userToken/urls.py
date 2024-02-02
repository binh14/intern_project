from django.urls import path
from userToken import views

urlpatterns = [
    path('check/', views.CheckView.as_view(), name='check_view'),
]
