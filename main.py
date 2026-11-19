
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date
import os
import shutil
import uuid

from database import engine, Base, SessionLocal
import models

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI()

# Create folder for uploaded files
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Connect static folder
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Connect HTML templates
templates = Jinja2Templates(directory="templates")




# Display homepage with search and filters
@app.get("/")
def home(
    request: Request,
    search: str = "",
    priority: str = "",
    status: str = ""
):
    db = SessionLocal()

    try:
        # Get all tasks for dashboard counters
        all_tasks = db.query(models.Task).all()

        total_tasks = len(all_tasks)
        completed_tasks = sum(1 for task in all_tasks if task.completed)
        pending_tasks = total_tasks - completed_tasks

        # Start building the task query
        query = db.query(models.Task)

        # Search tasks by name
        if search:
            query = query.filter(
                models.Task.title.ilike(f"%{search}%")
            )

        # Filter by priority
        if priority in ["low", "medium", "high"]:
            query = query.filter(
                models.Task.priority == priority
            )

        # Filter by completion status
        if status == "completed":
            query = query.filter(
                models.Task.completed == True
            )
        elif status == "pending":
            query = query.filter(
                models.Task.completed == False
            )

        # Get filtered tasks
        tasks = query.all()

        return templates.TemplateResponse(
            request=request,
            name="tasks.html",
            context={
                "tasks": tasks,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "search": search,
                "priority": priority,
                "status": status,
                "today": date.today()
            }
        )

    finally:
        db.close()



# Open the Edit Task page
@app.get("/edit-task/{task_id}")
def edit_task(request: Request, task_id: int):
    db = SessionLocal()

    try:
        task = db.query(models.Task).filter(
            models.Task.id == task_id
        ).first()

        if not task:
            return RedirectResponse(
                url=f"/#task-{task_id}",
                status_code=303
                )

        return templates.TemplateResponse(
            request=request,
            name="edit_task.html",
            context={"task": task}
        )

    finally:
        db.close()



# Add new task
@app.post("/add-task")
def add_task(
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    attachment: UploadFile = File(None)
):
    db = SessionLocal()

    try:
        title = title.strip()
        description = description.strip()

        if not title:
            return RedirectResponse(url="/", status_code=303)

        # Validate priority
        if priority not in ["low", "medium", "high"]:
            priority = "medium"

        # Convert due date
        task_due_date = None
        if due_date:
            try:
                task_due_date = date.fromisoformat(due_date)
            except ValueError:
                task_due_date = None

        # Save uploaded file
        attachment_path = None

        if attachment and attachment.filename:
            extension = os.path.splitext(attachment.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{extension}"

            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(attachment.file, buffer)

            attachment_path = f"/static/uploads/{unique_filename}"

        # Create new task
        new_task = models.Task(
            title=title,
            description=description,
            priority=priority,
            due_date=task_due_date,
            attachment=attachment_path
        )

        db.add(new_task)
        db.commit()

    finally:
        db.close()

    return RedirectResponse(url="/", status_code=303)



# Update an existing task
@app.post("/update-task/{task_id}")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
    due_date: str = Form("")
):
    db = SessionLocal()

    try:
        task = db.query(models.Task).filter(
            models.Task.id == task_id
        ).first()

        if not task:
            return RedirectResponse(url="/", status_code=303)

        task.title = title.strip()
        task.description = description.strip()

        if priority in ["low", "medium", "high"]:
            task.priority = priority

        if due_date:
            try:
                task.due_date = date.fromisoformat(due_date)
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None

        db.commit()

    finally:
        db.close()

    return RedirectResponse(url="/", status_code=303)


# Delete task
@app.post("/delete-task/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(models.Task).filter(
            models.Task.id == task_id
        ).first()

        if task:
            db.delete(task)
            db.commit()
    finally:
        db.close()

    return RedirectResponse(url="/", status_code=303)


# Mark task as completed
@app.post("/complete-task/{task_id}")
def complete_task(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(models.Task).filter(
            models.Task.id == task_id
        ).first()

        if task:
            task.completed = True
            db.commit()
    finally:
        db.close()

    return RedirectResponse(url="/", status_code=303)
