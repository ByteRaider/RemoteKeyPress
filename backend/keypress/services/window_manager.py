from pywinauto.application import Application
import pywinauto
from pywinauto import Desktop
from rest_framework.response import Response
from rest_framework import status
import time


class WindowManager:

    def click_button(self, window, button_name):
        try:
            button = window[button_name]
            button.click()
            return True
        except Exception as e:
            return False
    def click_checkbox(self, window, checkbox_name):
        try:
            checkbox = window[checkbox_name]
            checkbox.click()
            return True
        except Exception as e:
            return False
    def click_radio_button(self, window, radio_button_name):
        try:
            radio_button = window[radio_button_name]
            radio_button.click()
            return True
        except Exception as e:
            return False

    def find_window(self, title):
    # Find the window with the given title
        try:
            window = self.app.window(best_match=title)
            return window
        except Exception as e:
            return None

    def find_windows(self, request):
    # returns a list of all the top level windows in the application
        if 'selected_app' in request.session:
            app = Application().connect(best_match=request.session['selected_app'])
            windows = app.windows()
            return f'"windows":"{windows}"'
        else:
            return Response({'status': 'error', 'message': 'No application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)
     

   
    def find_window_handles(self, request):
    # Return a list of handles of all the top level windows in the application 
            if 'selected_app' in request.session:
                app = Application().connect(best_match=request.session['selected_app'])
                windows = app.windows()
                handles = [(window.window_text(),window.friendly_class_name(), window.handle) for window in windows]
                return f'"handles":"{handles}"'
            else:
                return Response({'status': 'error', 'message': 'No application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)
        # Brings  selected application to the front
    def window_to_foreground(self, request):
    # Brings  selected application to the front
                if 'selected_app' in request.session:
                    app = Application().connect(best_match=request.session['selected_app'])
                    app.top_window().set_focus()
                    return Response({'status': 'success', 'message': f'Application {request.session["selected_app"]} brought to the front.'})
                else:
                    return Response({'status': 'error', 'message': 'No application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)
            # Brings  selected application to the top left corner of the screen
    def window_to_top_left(self, request):
    # Brings  selected application to the top left corner of the screen
                if 'selected_app' in request.session:
                    app = Application().connect(best_match=request.session['selected_app'])
                    window = app.window(best_match=request.session['selected_app'])
                    window.move_window(0, 0)
                    return Response({'status': 'success', 'message': f'Application {request.session["selected_app"]} brought to the top left corner of the screen.'})
                else:
                    return Response({'status': 'error', 'message': 'No application window is selected.'}, status=status.HTTP_400_BAD_REQUEST)


    def __init__(self):
        pass