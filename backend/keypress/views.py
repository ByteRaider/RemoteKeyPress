from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyautogui
#from pywinauto.application import Application
import pywinauto
#from pywinauto import Desktop
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CheckboxActionSerializer, ApplicationListSerializer

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
    def get(self, request):
        windows = Desktop(backend="uia").windows()
        window_titles = [window.window_text() for window in windows]
        serializer = ApplicationListSerializer({'windows': window_titles})
        return Response(serializer.data)

class SelectApplicationView(APIView):
    def post(self, request):
        title = request.data.get('title')
        try:
            app = Application().connect(title=title)
            request.session['selected_app'] = title
            return Response({'status': 'success', 'message': f'Application {title} selected.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckboxControlView(APIView):
    def post(self, request):
        serializer = CheckboxActionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            #title = serializer.validated_data['title']
            #action = serializer.validated_data['action']

            try:
                # Connect to the application
                app = Application().connect(title="Your Application Title")
                main_window = app.window(title="Your Application Title")
                
                # Find the checkbox and perform the action
    #            checkbox = main_window.child_window(title=title, control_type="CheckBox")
    #            if action == 'check' and not checkbox.is_checked():
    #                checkbox.check()
    #            elif action == 'uncheck' and checkbox.is_checked():
    #                checkbox.uncheck()

    #            return Response({'status': 'success', 'message': f'{title} has been {action}ed.'})
    #        except Exception as e:
    #            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Process each checkbox action in the request
                responses = []
                for checkbox_action in serializer.validated_data:
                    title = checkbox_action['title']
                    action = checkbox_action['action']
                    checkbox = main_window.child_window(title=title, control_type="CheckBox")

                    # Perform the action based on the request
                    if action == 'check' and not checkbox.is_checked():
                        checkbox.check()
                    elif action == 'uncheck' and checkbox.is_checked():
                        checkbox.uncheck()
                    responses.append({'title': title, 'action': action, 'status': 'success'})

                return Response(responses)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)