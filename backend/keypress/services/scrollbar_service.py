#from celery import shared_task
import pyautogui
import time

#@shared_task
def locate_scrollbar(image_path):
    try:
        # Wait for the screen to stabilize
        time.sleep(1)
        # Locate the scrollbar on the screen
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            return {
                'status': 'success',
                'position': location._asdict()  # Convert to dictionary
            }
        else:
            return {'status': 'not_found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

