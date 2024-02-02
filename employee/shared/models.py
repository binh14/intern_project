from django.db import models

class BaseModels(models.Model):
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class SoftDeleteModels(models.Model):
    is_deleted = models.BooleanField(default = False)

    class Meta:
        abstract = True