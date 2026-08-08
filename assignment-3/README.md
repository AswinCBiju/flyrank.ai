# Assignment 3 - Task API Dockerization with PostgreSQL

A fully containerized RESTful Task Management application built with **FastAPI** and **PostgreSQL**, orchestrated using **Docker** and **Docker Compose**.

This assignment extends the Task API by migrating the persistence layer to a PostgreSQL database container with volume persistence and automated database initialization.

---

## 🏗️ Architecture & Stack

- **Web Service**: FastAPI running on Python 3.11 (`uvicorn`).
- **Database**: PostgreSQL 15 (`postgres:15-alpine`).
- **Orchestration**: Docker Compose with healthcheck dependency mapping.
- **Persistence**: Named Docker volume (`pgdata`) ensuring data survives container lifecycle restarts.
- **Auto-Initialization**: Database schema and seed data mounted via `init.sql` into `/docker-entrypoint-initdb.d/`.

---

## 🛠️ Project Structure

```text
assignment-3/
│
├── .env                  # Active environment configuration (git ignored)
├── .env.example          # Template environment variable configurations
├── Dockerfile            # Container build specification for FastAPI app
├── docker-compose.yml    # Multi-container service specification (web + db)
├── init.sql              # Database table creation and initial seed data
├── main.py               # FastAPI application endpoints & logic
├── requirements.txt      # Python dependencies (FastAPI, uvicorn, psycopg2-binary, etc.)
└── README.md             # Project documentation
```

---

## ⚙️ Environment Variables Configuration

Create a `.env` file in the root directory (or copy from `.env.example`):

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=taskdb
DB_USER=postgres
DB_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskdb
```

---

## 🚀 Running the Stack with Docker Compose

### 1. Build and Start Services
Run the following command to build the web image and start both the database and web containers in detached mode:

```bash
docker compose up --build -d
```

*(If using older docker-compose syntax, use `docker-compose up --build -d`)*

### 2. View Service Logs
To monitor container logs:

```bash
# View all logs
docker compose logs -f

# View web app logs only
docker compose logs -f web

# View database logs only
docker compose logs -f db
```

### 3. Check Container Status
Verify that both containers are running and the database is healthy:

```bash
docker compose ps
```

### 4. Stop Services
To stop running containers without losing database data:

```bash
docker compose stop
```

To bring down containers and networks:

```bash
docker compose down
```

To remove containers and wipe persistent database volumes:

```bash
docker compose down -v
```

---

## 📌 API Endpoints & Usage

Once running, access the interactive API documentation at:
👉 **`http://localhost:8000/docs`** (Swagger UI) or **`http://localhost:8000/redoc`**

| Method | Endpoint | Description | Expected Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Root / Meta Info | `200 OK` |
| `GET` | `/health` | Health Check Endpoint | `200 OK` |
| `GET` | `/tasks` | Retrieve all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve a task by ID | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update an existing task | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task by ID | `200 OK` / `404 Not Found` |

---

## 🧪 Verification & Inspection

### Access PostgreSQL CLI Inside Container
You can query the database directly inside the running container:

```bash
docker exec -it task_postgres psql -U postgres -d taskdb
```

Sample SQL queries inside `psql`:

```sql
\dt                  -- List tables
SELECT * FROM tasks; -- Query stored tasks
\q                   -- Exit psql
```

### Data Persistence Verification
1. Start the stack: `docker compose up -d`
2. Create a task using `POST /tasks` or Swagger UI.
3. Restart the containers: `docker compose restart`
4. Fetch tasks (`GET /tasks`) to verify created data persists across restarts.
