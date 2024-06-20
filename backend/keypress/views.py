from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyautogui
from pywinauto.application import Application
import pywinauto
from pywinauto import Desktop
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CheckboxActionSerializer, ApplicationListSerializer, WindowDescendantsSerializer

@csrf_exempt
def trigger_key(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            key = data.get('key')
            if key:
                pyautogui.press(key)
                return JsonResponse({'status': 'success', 'message': f'Key {key} pressed'})
            else:
                return JsonResponse({'status': 'fail', 'message': 'Key not provided'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ListApplicationsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        #windows = Desktop(backend="uia").windows()
        windows = Desktop(backend="win32").windows()
        
        window_titles = [window.window_text() for window in windows]
        serializer = ApplicationListSerializer({'windows': window_titles})
        return Response(serializer.data)
    

class SelectApplicationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        title = request.data.get('title')
        try:
            app = Application().connect(title=title)
            request.session['selected_app'] = title
            return Response({'status': 'success', 'message': f'Application {title} selected.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FindDescendantsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Connect to the application
            app_title = 'Rise of Kingdoms Bot 1.0.5.4'
            app = Application().connect(best_match=app_title)
            main_window = app.window(best_match=app_title)
            
            # Find all descendants of the main window 
            descendants_raw = main_window.descendants()
            descendants = []

            # Find all descendants of the main window and append to descendants list
            for descendant in descendants_raw:
                descendant_info = {'title': descendant.window_text()}
                if hasattr(descendant, 'control_type'):
                    descendant_info['control_type'] = descendant.control_type()
                if hasattr(descendant, 'automation_id'):
                    descendant_info['automation_id'] = descendant.automation_id()
                if hasattr(descendant, 'rectangle'):
                    rect = descendant.rectangle()
                    descendant_info['rectangle'] = {
                        'left': rect.left,
                        'top': rect.top,
                        'right': rect.right,
                        'bottom': rect.bottom
                    }
                if hasattr(descendant, 'is_enabled'):
                    descendant_info['enabled'] = descendant.is_enabled()
                if hasattr(descendant, 'is_visible'):
                    descendant_info['visible'] = descendant.is_visible()
                if hasattr(descendant, 'class_name'):
                    descendant_info['class_name'] = descendant.class_name()
                if hasattr(descendant, 'handle'):
                    descendant_info['handle'] = descendant.handle
                
                descendants.append(descendant_info)

            # Return the data as a response
            return Response({'status': 'success', 'descendants': descendants})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
