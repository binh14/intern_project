from django.db import models
from user.models import User

# Create your models here.
class UserToken(models.Model):
    email = User.email
    user_type = User.user_type
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_token_id = models.CharField(max_length=255, null = False)
    code = models.CharField(max_length=6, null=False)
    experied = models.DateTimeField(null = False)
    
# class CheckInput(models.Model):
#     email = models.EmailField(unique=True, null=False)
#     user_type = models.CharField(max_length=30, null=False)