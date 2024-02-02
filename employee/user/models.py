from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModels, SoftDeleteModels
from user.enum import UserType
# Create your models here.
class User(AbstractUser, BaseModels, SoftDeleteModels):

    phone_number = models.CharField(max_length = 20, null = False)
    user_type = models.CharField(
        choices = UserType.choices,
        default = UserType.EMPLOYEE,
        max_length = 30
    )
    