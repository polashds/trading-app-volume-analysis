import os
from pathlib import Path

project_name = "trading-app"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/templates/__init__.py",
    f"{project_name}/templates/index.html",
    f"{project_name}/templates/layout.html",
    f"{project_name}/templates/404.html",
    f"{project_name}/static/__init__.py",
    f"{project_name}/static/css/__init__.py",
    f"{project_name}/static/css/style.css",
    f"{project_name}/static/js/__init__.py",
    f"{project_name}/static/js/script.js",
    f"{project_name}/static/favicon.ico",
    "README.md",
    "LICENSE",
    "app.py",
    "requirements.txt",
    "config.py",
    "tasks.py",
    "database.py",
    ".gitignore",
    
]


for file in list_of_files:
    file_path = Path(file)

    filedir, filename = os.path.split(file_path)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(file)) or (os.path.getsize(file) == 0):
        with open(file, "w") as f:
            pass

    else:
        print(f"{filename} already exists")