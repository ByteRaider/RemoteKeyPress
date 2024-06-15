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
