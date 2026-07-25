# Assignment 2 - Task API with SQLite Persistence

A RESTful Task Management API built with **FastAPI** and **SQLite**. This API provides full CRUD (Create, Read, Update, Delete) functionality for task management, persisting all data across server restarts.

---

## 🚀 Features

- **SQLite Persistence**: Replaces in-memory storage; data survives server restarts.
- **Auto-Initialization**: Database directory and `tasks` table are automatically created on server start if missing.
- **First-Run Seeding**: Automatically seeds three initial tasks (`Learn FastAPI`, `Build CRUD API`, `Push project to GitHub`) only on the first run.
- **Pure SQL Queries**: All database operations use explicit SQL queries.
- **Error Handling**: 
  - `404 Not Found` for non-existent task IDs.
  - `400 Bad Request` / `422 Unprocessable Entity` for invalid payloads or missing fields.

---

## 📁 Project Structure

```text
assignment-2/
│
├── main.py              # FastAPI application with endpoints & SQLite operations
├── database/            # SQLite database folder (auto-generated)
│   └── tasks.db         # SQLite database file
├── README.md            # Project documentation
└── docs/                # Screenshots and documentation assets
    └── db_screenshot.png # Database inspection screenshot
```

---

## 🛠️ Requirements & Installation

1. **Python 3.8+**
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

---

## 🏃 Running the Server

Start the API server locally using Uvicorn:

```bash
uvicorn main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

Interactive API documentation (Swagger UI) is available at:
👉 **`http://127.0.0.1:8000/docs`**

---

## 📌 API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Root / Info | `200 OK` |
| `GET` | `/health` | Health Check | `200 OK` |
| `GET` | `/tasks` | Retrieve all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve a specific task by ID | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `201 Created` / `422 Unprocessable Entity` |
| `PUT` | `/tasks/{id}` | Update an existing task's title or status | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task by ID | `200 OK` / `404 Not Found` |

### Example Request Body (POST /tasks)
```json
{
  "title": "Finish Assignment 2"
}
```

### Example Request Body (PUT /tasks/{id})
```json
{
  "title": "Finish Assignment 2",
  "done": true
}
```

---

## 📸 Database Verification Screenshot

![Database Screenshot](docs/db_screenshot.png)

*(Note: Replace `docs/db_screenshot.png` with a screenshot showing your SQLite DB browser / CLI query of the `tasks` table).*
