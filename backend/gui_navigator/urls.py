from django.urls import path
from .views import ScrollbarAPIView
app_name = 'gui_navigator'
urlpatterns = [
    path('scrollbar/', ScrollbarAPIView.as_view(), name='scrollbar_api'),
]
