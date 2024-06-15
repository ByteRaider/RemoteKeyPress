from django.urls import path
from . import views

urlpatterns = [
    path('trigger/', views.trigger_key, name='trigger_key'),
]
