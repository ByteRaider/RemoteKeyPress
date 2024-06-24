from django.contrib import admin
from django.urls import path, include

from keypress.urls import urlpatterns as keypress_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # browsable API rest framework
    path('keypress/', include('keypress.urls', namespace='keypress')), # 
]
