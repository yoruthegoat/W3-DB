# Task API

## Install & run

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && fastapi dev main.py
```

Windows: use `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.

Runs at `http://127.0.0.1:8000`. Docs at `/docs`.

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

## Example

```
$ curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Buy milk"}'

HTTP/1.1 201 Created
date: Thu, 03 Sep 2026 07:23:29 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger

`/docs`

