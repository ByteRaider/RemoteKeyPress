from django.urls import path
from . import views
app_name = 'keypress'
urlpatterns = [

    path('trigger/', views.trigger_key, name='trigger_key'),
    path('list-applications/', views.ListApplicationsView.as_view(), name='list-applications'),
    path('select-application/', views.SelectApplicationView.as_view(), name='select-application'),
    path('descendants/', views.FindDescendantsView.as_view(), name='descendants'),
    path('application-windows/', views.ApplicationWindowsView.as_view(), name='application-windows'),
]
