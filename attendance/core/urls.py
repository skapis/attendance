from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance, name='attendance'),
    path('attendance/<uuid:id>/edit', views.edit_attendance, name='edit_attendance'),
    path('attendance/<uuid:id>/delete', views.delete_attendance, name='delete_attendance'),
    path('confirm', views.confirm_attendance, name='confirm_attendance')
]