from django.urls import path
from leaveRequest import views

urlpatterns = [
    path('leaveRequest/', views.ListCreateLeaveRequestView.as_view()),
    # path('leaveRequest/<int:pk>', views.UpdateDeleteLeaveRequestView.as_view()),

    path('create-leave-request/', views.CreateLeaveRequestView.as_view(), name = "create_leave_requeset"),

    path('leave-request/<int:leave_request_id>/', views.GetUpdateDeleteLeaveRequestView.as_view(), name = "get_detail")

]