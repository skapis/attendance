import uuid
from datetime import datetime as dt
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    projectId = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    start = models.TimeField()
    end = models.TimeField()
    duration = models.IntegerField(null=True)
    created = models.DateTimeField(default=now)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} - {self.name}"

    def work_hours(self):
        hours = round(self.duration/3600, 2)
        return hours

    def save(self, *args, **kwargs):
        start_time = dt.strptime(str(self.start), '%H:%M:%S')
        end_time = dt.strptime(str(self.end), '%H:%M:%S')
        year = dt.strptime(str(self.date), '%Y-%m-%d').year
        month = dt.strptime(str(self.date), '%Y-%m-%d').month
        hours = end_time - start_time
        self.duration = hours.total_seconds()
        self.year = year
        self.month = month
        super(Project, self).save(*args, **kwargs)


class ProjectsAggMonth(models.Model):
    monthId = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    month = models.DateField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name}|{self.month} - {self.first_name} {self.last_name}"

    def hours(self):
        return round(self.duration/3600, 2)







