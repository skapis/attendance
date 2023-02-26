from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('userprofile.urls')),
    path('auth/', include('authentication.urls')),
    path('projects/', include('projects.urls')),
    path('staff/', include('staff.urls'))
]
