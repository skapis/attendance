from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<uuid:id>/edit', views.edit_project, name='edit_project'),
    path('export', views.export_to_excel, name='excel_export'),
    path('confirm', views.confirm_projects, name='confirm')

]