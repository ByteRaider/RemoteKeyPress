# RemoteKeyPress Django Backend

This is the backend for the RemoteKeyPress project, built with Django. It provides an API to trigger key presses on a remote computer, as well as to list application running and it's options.

## Features

- List Open applications
- List Options for selected application
- Trigger key presses remotely via an HTTP API.

## Prerequisites

- Python 3.7+
- Django 3.0+
- `pyautogui` library

## Installation

1. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

# API Endpoint usage:

## Pass keyboard key press

- **URL**: `/keypress/trigger/`
- **Method**: POST
- **Payload**: JSON object containing the key to press

### Example Request

```python
import requests

url = 'http://remote-computer-ip:8000/keypress/trigger/'
data = {'key': 'a'}

response = requests.post(url, json=data)
print(response.text)
```

## List Active Application Windows

- **URL**: `/keypress/list-applications/`
- **Method**: GET http://your.server.IP.address:8000/keypress/list-applications/

## Select Application Window

- **URL**: `/keypress/select-application/`
- **Method**: POST http://your.server.IP.address:8000/keypress/select-application/
- **Payload**: JSON object containing the name of the application window

### Example Request

```
{
"title":"Calculator"
}
```

## Find Descendents inside selected application window

- **URL**: `/keypress/descendants`
- **Method**: GET http://your.server.IP.address:8000/keypress/descendants/

## List all the windows inside the application

- **URL**: `/keypress/application-windows/`
- **Method**: GET http://your.server.IP.address:8000//keypress/application-windows/

## List all the control identifiers

- **URL**: `control-identifiers/`
- **Method**: GET http://your.server.IP.address:8000//keypress/control-identifiers/
