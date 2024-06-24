# services/window_manager.py

from pywinauto.application import Application
from rest_framework.response import Response
from rest_framework import status


class WindowManager:

    def __init__(self, request):
        self.request = request
        if 'selected_app' in request.session:
            self.app = Application().connect(best_match=request.session['selected_app'])
            self.title = request.session['selected_app']
            self.window = self.app.window(best_match=self.title)

        else:
            self.app = None
            self.window = None

    def find_window(self, title):
        try:
            window = self.app.window(best_match=title)
            return window
        except Exception as e:
            #return None
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def find_windows(self):
        try:
            windows = self.app.windows()
            return windows
        except Exception as e:
            return None

    def find_window_handles(self):
        try:
            windows = self.app.windows()
            handles = [(window.window_text(), window.friendly_class_name(), window.handle) for window in windows]
            return handles
        except Exception as e:
            return None

    def find_buttons(self):
        try:
            buttons = self.window.descendants(control_type="Button")
            return buttons
        except Exception as e:
            return None

    def find_checkboxes(self):
        try:
            checkboxes = self.window.descendants(control_type="CheckBox")
            return checkboxes
        except Exception as e:
            return None

    def find_radiobuttons(self):
        try:
            radiobuttons = self.window.descendants(control_type="RadioButton")
            return radiobuttons
        except Exception as e:
            return None

    def find_textboxes(self):
        try:
            textboxes = self.window.descendants(control_type="Edit")
            return textboxes
        except Exception as e:
            return None
    def find_scrlollbars(self):
        try:
            scrollbars = self.window.descendants(control_type="ScrollBar")
            return scrollbars
        except Exception as e:
            return None

    def scroll_to_top(self):
        try:
            self.window.scroll_to_point(0, 0)
            return True
        except Exception as e:
            return False
    def scroll_to_bottom(self):
        try:
            self.window.scroll_to_point(0, 1000000)
            return True
        except Exception as e:
            return False
    def scroll_to_middle(self):
        try:
            self.window.scroll_to_point(0, 500000)
            return True
        except Exception as e:
            return False
    
    def click_button(self, button_name):
        try:
            button = self.window[button_name]
            button.click()
            return True
        except Exception as e:
            return False

    def click_textbox(self, textbox_name):
        try:
            textbox = self.window[textbox_name]
            textbox.set_focus()
            return True
        except Exception as e:
            return False

    def click_checkbox(self, checkbox_name):
        try:
            checkbox = self.window[checkbox_name]
            checkbox.click()
            return True
        except Exception as e:
            return False

    def click_radio_button(self, radio_button_name):
        try:
            radio_button = self.window[radio_button_name]
            radio_button.click()
            return True
        except Exception as e:
            return False

    def window_to_foreground(self):
        try:
            self.app.top_window().set_focus()
            return Response({'status': 'success', 'message': f'Application {self.request.session["selected_app"]} brought to the front.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def window_to_top_left(self):
        try:
            self.window.move_window(0, 0)
            return Response({'status': 'success', 'message': f'Application {self.request.session["selected_app"]} brought to the top left corner of the screen.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

