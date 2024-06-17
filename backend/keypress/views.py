from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyautogui
from rest_framework.response import Response
from pywinauto.application import Application
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CheckboxActionSerializer

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


class CheckboxControlView(APIView):
    def post(self, request):
        serializer = CheckboxActionSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            action = serializer.validated_data['action']

            try:
                # Connect to the application
                app = Application().connect(title="Your Application Title")
                main_window = app.window(title="Your Application Title")
                
                # Find the checkbox and perform the action
                checkbox = main_window.child_window(title=title, control_type="CheckBox")
                if action == 'check' and not checkbox.is_checked():
                    checkbox.check()
                elif action == 'uncheck' and checkbox.is_checked():
                    checkbox.uncheck()

                return Response({'status': 'success', 'message': f'{title} has been {action}ed.'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)