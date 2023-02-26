import decimal
import uuid
from datetime import datetime as dt, time, timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile


class AttendanceCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Attendance(models.Model):
    attendanceId = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(to=AttendanceCategory, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    duration = models.IntegerField(null=True)
    created = models.DateTimeField(default=now)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.owner.first_name} {self.owner.last_name}"

    def saldo(self):
        required = self.profile.fteValue * decimal.Decimal(8.5)
        hours = self.work_hours()
        saldo = decimal.Decimal(hours) - required
        return round(saldo, 2)

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
        super(Attendance, self).save(*args, **kwargs)


class Calendar(models.Model):
    date = models.DateField()
    month = models.IntegerField()
    year = models.IntegerField()
    weekend = models.BooleanField()
    holiday = models.BooleanField()

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Calendar'

    def __str__(self):
        return str(self.date)


class AttendanceAggMonth(models.Model):
    monthId = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    month = models.DateField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.month} - {self.first_name} {self.last_name}"

    def hours(self):
        return round(self.duration/3600, 2)



