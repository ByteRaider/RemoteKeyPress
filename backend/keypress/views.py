from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyautogui

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
                return JsonResponse({'status': 'fail', 'message': 'Key not provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)
