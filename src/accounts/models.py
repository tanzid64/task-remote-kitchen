import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    class UserType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', _('Customer')
        OWNER = 'OWNER', _('Owner')
        EMPLOYEE = 'EMPLOYEE', _('Employee')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(
        _("User Type"),
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    
    def __str__(self):
        return self.username