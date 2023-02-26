from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='staff'),
    path('employee/<uuid:id>', views.emp_detail, name='employee'),
    path('access-denied', views.access_denied, name='access_denied'),
    path('new-user', views.create_new_user, name='new_user'),
    path('check-user', views.check_user, name='check_user'),
    path('user-active/<uuid:id>', views.toggle_user_active, name='user_active'),
    path('attendance/<uuid:id>/edit', views.edit_emp_attendance, name='emp_att_edit'),
    path('projects/<uuid:id>/edit', views.edit_emp_projects, name='emp_project_edit'),
    path('projects/export/<uuid:id>', views.export_emp_projects, name='export_emp_projects'),
    path('attendance/export/<uuid:id>', views.export_emp_attendance, name='export_emp_attendance')
]
