from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = ('admin','Admin')
    WRITER = ('writer','Writer')
    READER=('reader','Reader')

class CustomUser(AbstractUser):
    role=models.CharField(max_length=20,choices=Role,default=Role.READER)
    email = models.EmailField(unique=True, blank=False)


#parol
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
User = get_user_model()
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=2)

    def __str__(self):
        return f'{self.user.username} - {self.code}'
