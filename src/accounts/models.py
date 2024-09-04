import uuid
from django.db import models
from core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.constants import USER_TYPE, SHIFT
from django.core.exceptions import ValidationError
# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(
        _("User Type"),
        max_length=10,
        choices=USER_TYPE,
        default=USER_TYPE[0][0],
    )

class OwnerProfile(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_no = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user.user_type != "OWNER":
            raise ValidationError("Only an owner can create an owner profile")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username
    
class EmployeeProfile(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.CharField(
        _("Shift"),
        max_length=10,
        choices=SHIFT,
        default=SHIFT[0][0],
    )

    def save(self, *args, **kwargs):
        if self.user.user_type != "EMPLOYEE":
            raise ValidationError("Only an employee can create an employee profile")
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.user.username