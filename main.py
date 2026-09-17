# main reference: https://realpython.com/get-started-with-fastapi/
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI()

DB_FILE = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Eat", 1),
                ("Sleep", 1),
                ("Repeat", 1),
            ]
        )

    conn.commit()
    conn.close()

init_db()

tasks = [
    { "id": 1,
     "title":"Eat", 
     "done":True },
    { "id": 2,
     "title":"Sleep", 
     "done":True },
    { "id": 3,
     "title":"Repeat", 
     "done":True }

]

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

# catches: missing title, wrong type (e.g. title: 123), malformed JSON
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})

# override to return JSON errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.get("/")
def root():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] }

@app.get("/health")
def get_health():
    return { "status": "ok" }

@app.get("/tasks")
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    for task in result:
        # since sqlite just has 1s and 0s
        task["done"] = bool(task["done"])
    return result

@app.get("/tasks/{id}")
def get_task(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    task = dict(row)

    # since sqlite just has 1s and 0s
    task["done"] = bool(task["done"])
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def post_task(task: Task ):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )

    conn.commit()

    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
    new_task = dict(cursor.fetchone())
    new_task["done"] = bool(new_task["done"])
    conn.close()

    return new_task

@app.put("/tasks/{id}")
def put_task(id: int, update: TaskUpdate):
    if update.title is None and update.done is None:
        raise HTTPException(status_code=400, detail="Request body must include title and/or done")

    for task in tasks:
        if task["id"] == id:
            if update.title is not None:
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {id} not found")