# 🎬 Movie Reservation System (Backend)

> Backend REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** — currently under active development as part of my backend learning roadmap.

---

## 🚀 Overview

This project is a **backend service** for a Movie Reservation System.  
It allows users to manage movies, showtimes, and (coming soon) seat reservations.  

I’m building it to **master backend engineering** concepts:
- CRUD operations with FastAPI  
- Database modeling with SQLAlchemy  
- Data validation using Pydantic v2  
- Relationships (One-to-Many, Many-to-One)  
- REST API design best practices  

---

## 🧠 Learning Context

I'm a **Computer Science student in Belgium**,  
currently developing this backend as part of my personal learning path in **FastAPI + PostgreSQL**.  

My goal is to:
- Strengthen my backend fundamentals  
- Understand ORM relationships deeply  
- Learn how to build and structure production-ready APIs  
- Eventually connect this backend to a **Next.js frontend** (CineEntry-style project)

---

## ⚙️ Tech Stack

| Layer | Technology |
|--------|-------------|
| Framework | **FastAPI** |
| ORM | **SQLAlchemy** |
| Database | **PostgreSQL** |
| Validation | **Pydantic v2** |
| Server | **Uvicorn** |
| Docs | **Swagger / OpenAPI** |

---

## 📂 Current Features

### 🎞️ Movies
- Create, Read, Update, Delete movies  
- Schema-based validation  
- Clean error handling (404, validation, etc.)

### 🕒 Showtimes
- Linked to movies via `movie_id`  
- CRUD endpoints  
- Returns `movie_title` for each showtime  
- Pagination support (`skip`, `limit`)

---

## 🧱 Next Steps (in progress)

### 🚧 Reservation System
- Add `Reservation` model and routes  
- Link with users and showtimes  
- Handle seat availability and cancellation logic  

### 🔐 Authentication
- Implement JWT authentication  
- Add user roles (Admin / Customer)  
- Protect restricted routes  

### 🧰 DevOps
- Dockerize the app (FastAPI + Postgres)
- Unit tests with pytest  
- Deploy to Render / Railway  

---

## 🧩 Project Structure
app/
├── core/ # Config, constants, utils
├── routers/ # API route files
│ ├── movies.py
│ └── showtime.py
├── models/ # SQLAlchemy models
│ ├── movie.py
│ └── showtime.py
├── schemas/ # Pydantic schemas
│ ├── movie.py
│ └── showtime.py
├── database.py # DB setup and get_db()
└── main.py # App entrypoint

---

## 🧭 Learning Journey

This project is not finished yet — it evolves as I learn:
✅ FastAPI fundamentals
✅ SQLAlchemy relationships
✅ REST API design
🔜 Authentication and authorization
🔜 Database migrations and deployment

---

## 🧑‍💻 Setup (Local Development)

```bash
# Clone repository
git clone https://github.com/azizsebri3/movie-reservation-system.git
cd movie-reservation-system/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # On Linux/macOS
venv\Scripts\activate        # On Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

