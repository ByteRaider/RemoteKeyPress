from django.urls import path
from . import views
app_name = 'keypress'
urlpatterns = [
    # Usage: See README.md for more details
    path('trigger/', views.trigger_key, name='trigger_key'),
    path('list-applications/', views.ListApplicationsView.as_view(), name='list-applications'),
    path('select-application/', views.SelectApplicationView.as_view(), name='select-application'),
    path('descendants/', views.FindDescendantsView.as_view(), name='descendants'),
    path('application-windows/', views.ApplicationWindowsView.as_view(), name='application-windows'),
    path('screenshot/', views.ScreenshotView.as_view(), name='screenshot'),
    path('find-window/', views.FindWindowView.as_view(), name='find-window'),
    path('find-windows/', views.FindWindowsView.as_view(), name='find-windows'),

    # Beta
    path('find-window/<str:title>/', views.FindWindowView.as_view(), name='find-window'),
    path('window-to-foreground/', views.WindowToForegroundView.as_view(), name='window-to-foreground'),
    path('window-to-top-left/', views.WindowToTopLeftView.as_view(), name='window-to-top-left'),
    path('locate-scrollbar/', views.ScrollbarLocatorView.as_view(), name='locate-scrollbar'),

#Locate the scrollbar:
#curl -X POST http://localhost:8000/api/locate_scrollbar/ -d '{"scrollbar_image_name": "images/scrollbar_image.png", "action": "locate"}' -H "Content-Type: application/json"

#Scroll up:
#curl -X POST http://localhost:8000/api/locate_scrollbar/ -d '{"scrollbar_image_name": "images/scrollbar_image.png", "action": "up"}' -H "Content-Type: application/json"

#Scroll down:
#curl -X POST http://localhost:8000/api/locate_scrollbar/ -d '{"scrollbar_image_name": "images/scrollbar_image.png", "action": "down"}' -H "Content-Type: application/json"

#Scroll to the middle:
#curl -X POST http://localhost:8000/api/locate_scrollbar/ -d '{"scrollbar_image_name": "images/scrollbar_image.png", "action": "middle"}' -H "Content-Type: application/json"


    
    #Alfa
    path('click-button/', views.ClickButtonView.as_view(), name='click-button'),
    path('find-windows/', views.FindWindowsView.as_view(), name='find-windows'),

]
# Example Usage:
#    Find Window:
#
#    GET /find-window/MyWindowTitle/
#    Click Button:

#    POST /click-button/
#    Body: { "window_title": "MyWindowTitle", "button_name": "MyButtonName" }
#    Find Windows:

#    GET /find-windows/
#    Window to Foreground:

#    POST /window-to-foreground/
#    Body: { "session_key": "value" }
#    Window to Top Left:

#    POST /window-to-top-left/
#    Body: { "session_key": "value" }
