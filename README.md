# DB

## Install & run

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && fastapi dev main.py
```

Windows: use `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.

Runs at `http://127.0.0.1:8000`. Docs at `/docs`.

## Database

Uses SQLite (`tasks.db`) — a single file, no server to set up. The file and its `tasks` table are created automatically on first run, seeded with 3 example tasks. It's git-ignored, so a fresh clone regenerates it. Data survives server restarts.

Example query run in DB Browser:
```sql
SELECT * FROM tasks WHERE done = 1;
```
Returned all 3 seeded tasks, since they're all marked done by default.

<img width="1891" height="1011" alt="image" src="https://github.com/user-attachments/assets/cf0cbd95-e02a-40cf-93fd-c5780e5026c4" />


## Endpoints

| Method | Path          | Description             | Success | Errors                    |
|--------|---------------|--------------------------|---------|----------------------------|
| GET    | `/`           | API info                | 200     | —                          |
| GET    | `/health`     | Health check             | 200     | —                          |
| GET    | `/tasks`      | List tasks               | 200     | —                          |
| GET    | `/tasks/{id}` | Get one task             | 200     | 404                        |
| POST   | `/tasks`      | Create task              | 201     | 400 (missing/empty title)  |
| PUT    | `/tasks/{id}` | Update task              | 200     | 400 (empty body), 404      |
| DELETE | `/tasks/{id}` | Delete task              | 204     | 404                        |
