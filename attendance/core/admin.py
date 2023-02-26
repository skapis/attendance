from django.contrib import admin
from .models import AttendanceCategory, Attendance, Calendar

admin.site.register(Attendance)
admin.site.register(AttendanceCategory)
admin.site.register(Calendar)
