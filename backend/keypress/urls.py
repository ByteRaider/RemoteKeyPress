from django.urls import path
from . import views

urlpatterns = [
    path('trigger/', views.trigger_key, name='trigger_key'),
    path('checkbox/', views.CheckboxControlView.as_view(), name='checkbox'),
    path('list-applications/', views.ListApplicationsView.as_view(), name='list-applications'),
    path('select-application/', views.SelectApplicationView.as_view(), name='select-application'),


]
