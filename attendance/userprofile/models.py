import uuid
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    profileId = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    workerId = models.CharField(max_length=255)
    fteValue = models.DecimalField(default=1, decimal_places=1, max_digits=10)
    position = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name}"

    class Meta:
        ordering = ['-created']
