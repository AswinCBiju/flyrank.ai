# Assignment 4 - Task API Authentication & Authorization with Supabase

A RESTful API built with **FastAPI**, **PostgreSQL**, and **Supabase Authentication**. This project implements user registration, authentication, token-based session management, and reusable middleware route guards.

---

## Running the Service Locally

### 1. Start the Database Container
Ensure your PostgreSQL container is running:

```bash
docker start task_postgres
```

### 2. Run the FastAPI Server
Activate your virtual environment and start the development server:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

- Local Server: **`http://127.0.0.1:8000`**  
- Interactive API Docs: **`http://127.0.0.1:8000/docs`**

---

## Authentication & Middleware Guard

### 🛡️ Reusable Middleware Guard 🛡️ (`get_current_user`)
Implemented in `auth/auth.py` using FastAPI's `HTTPBearer` dependency injection:

- **Token Extraction**: Automatically extracts the `Bearer <token>` string from the `Authorization` request header.
- **Verification**: Verifies the JWT token with Supabase (`supabase.auth.get_user(token)`).
- **Security Enforcement**: Missing, invalid, or expired tokens immediately return a `401 Unauthorized` response (`{"detail": {"error": "Access Token required"}}`).
- **Route Protection**: Adding `user = Depends(get_current_user)` to any endpoint automatically secures it and injects the authenticated `user` object.

---

## API Endpoints

### Public Routes
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Information | `200 OK` |
| `GET` | `/health` | Server Health Check | `200 OK` |
| `GET` | `/public/info` | Unprotected Public Info | `200 OK` |

### Auth Routes (`/auth`)
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | Register a new user | `201 Created` / `400 Bad Request` |
| `POST` | `/auth/login` | Log in user & return Access Token | `200 OK` / `401 Unauthorized` |
| `POST` | `/auth/logout` | Sign out authenticated session | `204 No Content` |

### Protected Routes (Requires `Authorization: Bearer <token>`)
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/auth/protected/profile` | Returns authenticated user profile | `200 OK` / `401 Unauthorized` |
| `GET` | `/auth/protected/dashboard` | Returns protected dashboard data | `200 OK` / `401 Unauthorized` |

---

## Testing Checkpoints (`curl`)

```bash
# 1. Signup
curl -i -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}'

# 2. Login
curl -i -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}'

# 3. Protected Profile
curl -i http://127.0.0.1:8000/auth/protected/profile \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

# 4. Protected Dashboard
curl -i http://127.0.0.1:8000/auth/protected/dashboard \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

# 5. Logout
curl -i -X POST http://127.0.0.1:8000/auth/logout \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```
