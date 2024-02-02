from django.db import models

class Reason(models.TextChoices):
    SICK = "SICK"
    VACATION = "VACATION"
    FAMILY = "FAMILY"
    ACCIDENT = "ACCIDENT"
    NO_PERMISSION = "NO_PERMISSION"
    OTHER_REASON = "OTHER_REASON"
class Status(models.TextChoices):
    CHECKED = "CHECKED"
    NOT_CHECKED = "NOT_CHECKED"