# Task Manager

A simple web-based Task Manager built using FastAPI, Jinja2, HTML, CSS, and SQLite. This project is designed to help users manage daily tasks through a clean and simple web interface.

## Features

- Server-rendered web pages using Jinja2
- FastAPI backend
- External CSS styling
- Static file serving for CSS and images
- SQLite database integration (planned/in progress)
- Task creation and management (planned/in progress)

## Technologies Used

- Python
- FastAPI
- Jinja2
- HTML5
- CSS3
- SQLite
- SQLAlchemy

## Project Structure

```text
task_manager/
├── main.py
├── requirements.txt
├── README.md
├── templates/
│   └── tasks.html
└── static/
    ├── css/
    │   └── style.css
    └── images/
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project folder:

   ```bash
   cd task_manager
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python -m uvicorn main:app --reload
   ```

5. Open your browser and visit:

   http://127.0.0.1:8000/

## Project Goal

The goal of this project is to learn how to build and deploy a web application using FastAPI, Jinja2 templates, static files, and a database.

## Author

Created as a learning project using Python and FastAPI.
