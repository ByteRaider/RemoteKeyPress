# RemoteKeyPress

#### API that allows you to remotely trigger key presses on a cloud-hosted computer.

## Project structure

#### RemoteKeyPress

├── backend/
│ ├── core/
│ ├── keypress/
│ ├── manage.py
│ ├── requirements.txt
│ └── README.md
├── frontend/
│ ├── remotekeypress_flutter/
│ ├── android/
│ ├── ios/
│ ├── lib/
│ ├── test/
│ ├── pubspec.yaml
│ └── README.md
├── .gitignore
├── LICENSE
└── README.md

###Explanation of the Structure:

- backend/: Contains all files related to the Django backend.

  - core/: Django project directory.
  - keypress/: Django app directory.
  - manage.py: Django management script.
  - requirements.txt: List of Python dependencies.
  - README.md: Instructions specific to setting up and running the Django backend.

- frontend/: Contains all files related to the Flutter frontend.

  - remotekeypress_flutter/: Flutter project directory.
  - android/, ios/, lib/, test/: Standard Flutter project directories.
  - pubspec.yaml: Flutter project configuration file.
  - README.md: Instructions specific to setting up and running the Flutter frontend.

- .gitignore: Specifies intentionally untracked files to ignore.
- LICENSE: License for this project.
- README.md: README files that provide an overview of the project.

## Backend

The backend is built with Django and provides an API to trigger key presses on a remote computer.

### Setup

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Follow the instructions in the [backend README](backend/README.md) to set up and run the Django server.

## Frontend

The frontend is built with Flutter and provides a simple interface to send key press commands to the backend API.

### Setup

1. Navigate to the `frontend` directory:

   ```bash
   cd frontend/remotekeypress_flutter
   ```

2. Follow the instructions in the [frontend README](frontend/README.md) to set up and run the Flutter app.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flutter](https://flutter.dev/)
- [Django](https://www.djangoproject.com/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
