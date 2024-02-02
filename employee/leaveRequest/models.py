from django.db import models
from leaveRequest.enum import Reason, Status
from user.models import User
# Create your models here.
class LeaveRequest(models.Model):
    
    user = models.ForeignKey(User, on_delete =  models.CASCADE, related_name = "leaverequests", null = True)
    start_date = models.DateTimeField(null = False)
    end_date = models.DateTimeField(null = False)
    status = models.CharField(
        max_length=255,
        null = False,
        default = Status.NOT_CHECKED
    )
    rejected_reason = models.CharField(max_length=255, null = False)
    other_reason = models.CharField(max_length=255, null = False)
    reason = models.CharField(
        max_length=255,
        choices = Reason.choices,
        default = Reason.NO_PERMISSION
    )