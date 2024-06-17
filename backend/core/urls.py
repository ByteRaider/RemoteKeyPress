from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # browsable API rest framework
    path('keypress/', include('keypress.urls')),
]
