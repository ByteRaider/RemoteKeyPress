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
import time

from .services.window_manager import WindowManager
from .services.scrollbar_service import locate_scrollbar

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
    # Returns selected application
     # Return a list of handles of all the top level windows in the application
        if 'selected_app' in request.session:
            app = Application().connect(best_match=request.session['selected_app'])
            #window = app.window(best_match=request.session['selected_app'])
            #app.top_window().set_focus()
            #window.move_window(0, 0)
            return Response({'status': 'success', 'message': f'Application {request.session["selected_app"]} selected.'})
        else:
            return Response({'status': 'error', 'message': 'No application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)
        
    permission_classes = [AllowAny]
    def post(self, request):
        if 'selected_app' in request.session:
            del request.session['selected_app']
            # TODO: Remove scrollbar image name from the session
            #del request.session['scrollbar_image_name']
        title_raw = request.data.get('title')
        title = title_raw.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace(',', '').replace('.', '')

        try:
            app = Application().connect(best_match=title)
            if not app:
                return Response({'status': 'error', 'message': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
            request.session['selected_app'] = title

            #TODO: Get scrollbar image name from the application and store it in the session
            #request.session['scrollbar_image_name'] = app.window(best_match=title).scrollbar_image_name
 
            window = app.window(best_match=request.session['selected_app'])
            app.top_window().set_focus()
            window.move_window(0, 0)
            return Response({'status': 'success', 'message': f'Application {title} selected.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Brings  selected application to the front

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

################################
@csrf_exempt
def trigger_key(request):
# API to trigger a key press 
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

class ScreenshotView(APIView):
# API to take a screenshot of the main window
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # Connect to the application
            if 'selected_app' not in request.session:
                return Response({'status': 'error', 'message': 'No application window is selected, maybe try "/keypress/select-application/" instead'}, status=status.HTTP_400_BAD_REQUEST)
            app_title = request.session.get('selected_app')
            app = Application().connect(best_match=app_title)
            main_window = app.window(best_match=app_title)

            # Take screenshot of the main window
            screenshot = main_window.capture_as_image()
            # give the image a unique ID before saving it in static/temp folder
            image_id = id(screenshot)
            # Save the image in static/temp folder
            screenshot.save(f'static/temp/{image_id}.png')
            #create a dynamic link for the image
            image_link = f'http://{request.META["HTTP_HOST"]}:8000/static/temp/{image_id}.png'
            return Response({'status': 'success', 'message': 'Screenshot taken.', 'image_link': image_link})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)      

# API to take a screenshot by handle
class ScreenshotByHandleView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, handle):
        if not handle:
            return Response({'status': 'error', 'message': 'Handle not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Connect to the application
            app = Application().connect(handle=handle)
            main_window = app.window(handle=handle)

            # Take screenshot of the main window
            screenshot = main_window.capture_as_image()
            # give the image a unique ID before saving it in static/temp folder
            image_id = id(screenshot)
            # Save the image in static/temp folder
            screenshot.save(f'static/temp/{image_id}.png')
            #create a dynamic link for the image
            image_link = f'http://{request.META["HTTP_HOST"]}:8000/static/temp/{image_id}.png'
            return Response({'status': 'success', 'message': 'Screenshot taken.', 'image_link': image_link})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#### WINDOW MANAGER ###
class FindWindowView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, **kwargs):
        if 'window_title' in kwargs:
            title = kwargs['window_title']
        else:
            title = request.session.get('selected_app')
        window_manager = WindowManager(request)
        window = window_manager.find_window(title)
        
        if window:
            return Response({"status": "success", "message": f"Window '{title}' found."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": f"Window '{title}' not found."}, status=status.HTTP_404_NOT_FOUND)


class FindWindowsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        window_manager = WindowManager(request)
        windows = window_manager.find_windows(request)
        
        return Response({"status": "success", "windows": windows}, status=status.HTTP_200_OK)

class WindowToForegroundView(APIView):
    def post(self, request):
        window_manager = WindowManager(request)
        response = window_manager.window_to_foreground(request)
        return response

class WindowToTopLeftView(APIView):
    def post(self, request):
        window_manager = WindowManager(request)
        response = window_manager.window_to_top_left(request)
        return response

### Buttons ###
class ClickButtonView(APIView):
# API to click a button in a window
    def post(self, request):
        window_title = request.data.get('window_title')
        button_name = request.data.get('button_name')

        window_manager = WindowManager(request)
        window = window_manager.find_window(window_title)
        
        if window:
            success = window_manager.click_button(window, button_name)
            if success:
                return Response({"status": "success", "message": f"Button '{button_name}' clicked in window '{window_title}'."}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": f"Failed to click button '{button_name}' in window '{window_title}'."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "message": f"Window '{window_title}' not found."}, status=status.HTTP_404_NOT_FOUND)

### Find buttons to connect to ###  
class FindButtonsView(APIView):
    def get(self, request):
        window_manager = WindowManager(request)
        buttons = window_manager.find_buttons()
        
        return Response({"status": "success", "buttons": buttons}, status=status.HTTP_200_OK)


#### Scrolling ####

class ScrollbarLocatorView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        return Response({'message': 'Task initiated'})
        
    def post(self, request, *args, **kwargs):
        #image_path = request.data.get('image_path')

        image_path = 'static/samples/rok_scroll_1.png'

        # Check if image_path is provided

        if not image_path:
            return Response({'error': 'Image path is required'}, status=400)
        
        # Trigger Celery task
        #task_result = locate_scrollbar.delay(image_path)

        task_result = locate_scrollbar(image_path)
        print("Task Result:", task_result)  # Add this to log the output
        print ("Task result type:", type(task_result)) # Add this to log the output

        return Response({task_result['status']: task_result['position']})