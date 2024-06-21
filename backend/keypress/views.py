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
from .serializers import ApplicationListSerializer, WindowSerializer

@csrf_exempt
# API to trigger a key press 
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

# API to list all applications in the desktop 
class ListApplicationsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        #windows = Desktop(backend="uia").windows()
        windows = Desktop(backend="win32").windows()
        
        window_titles = [window.window_text() for window in windows]
        serializer = ApplicationListSerializer({'windows': window_titles})
        return Response(serializer.data)
    
# API to select an application 
class SelectApplicationView(APIView):
    def get(self, request):
        if 'selected_app' in request.session:
            return Response({'status': 'success', 'message': f'Application {request.session["selected_app"]} selected.'})
        else:
            return Response({'status': 'error', 'message': 'No  application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [AllowAny]
    def post(self, request):
        if 'selected_app' in request.session:
            del request.session['selected_app']
        title_found = request.data.get('title')
        title = title_found.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace(',', '').replace('.', '')

        try:
            app = Application().connect(best_match=title)
            if not app:
                return Response({'status': 'error', 'message': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
            request.session['selected_app'] = title
            return Response({'status': 'success', 'message': f'Application {title} selected.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API to find all windows in the application
class ApplicationWindowsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if 'selected_app' not in request.session:
            return Response({'status': 'error', 'message': 'No application window is selected, maybe try "/keypress/select-application/" instead'}, status=status.HTTP_400_BAD_REQUEST)

        app_title = request.session.get('selected_app')
        app = Application().connect(best_match=app_title)
        windows = app.windows()

        window_data = [{
            'title': window.window_text(),
            'class_name': window.friendly_class_name(),
            'handle': window.handle
        } for window in windows]

        serializer = WindowSerializer(window_data, many=True)

        return Response({'status': 'success', 'windows': serializer.data})

# API to find all descendants of the main window
class FindDescendantsView(APIView):
    permission_classes = [AllowAny]
    # Find all descendants of the main window
    def get(self, request):
        try:
            # Connect to the application
            #app_title = 'Rise of Kingdoms Bot 1.0.5.4'
            if 'selected_app' not in request.session:
                return Response({'status': 'error', 'message': 'No application window is selected, maybe try "/keypress/select-application/" instead'}, status=status.HTTP_400_BAD_REQUEST)
            app_title = request.session.get('selected_app')
            app = Application().connect(best_match=app_title)
            main_window = app.window(best_match=app_title)
            
            # Find all descendants of the main window 
            descendants_raw = main_window.descendants()
            descendants = []

            # Find all descendants of the main window and append to descendants list
            for descendant in descendants_raw:


                descendant_info = {}
                if hasattr(descendant, 'title'):
                    descendant_info['title'] = descendant.title() or descendant.window_text()
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

