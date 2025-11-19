# 🚀 NXGFitTrack API  
A FastAPI backend for the NXG FitTrack mobile app — providing authentication, user profiles, workout templates, exercises, and workout history tracking.

---

## 📌 Overview  
NXGFitTrack API is designed to power a fitness-tracking mobile app where users can:

- Register & log in securely
- Manage their profile
- Create workout templates
- Add exercises to workouts
- Track completed workouts
- View history and progress

This API uses **FastAPI**, **JWT authentication**, **PostgreSQL**, and **SQLAlchemy ORM**.

---

## 🛠️ Tech Stack

- **FastAPI**
- **Python 3.10+**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Alembic (Optional)**
- **Pydantic**
- **JWT Auth**
- **Uvicorn**

---

## 📁 Project Structure

app/
│── main.py
│── models/
│── schemas/
│── crud/
│── deps.py
│── auth.py
│── routes/
│ ├── auth.py
│ ├── users.py
│ ├── workouts.py
│ └── history.py
│── database.py
│── utils/
│
requirements.txt

# 🚀 Getting Started

## 1️⃣ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/NXGFitTrack-API.git
cd NXGFitTrack-API
```
## 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```
## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 🗄️ Environment Configuration
Create .env file:
```bash
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/nxgfittrack
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
```
## ▶️ Run the Server
```bash
uvicorn app.main:app --reload
or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


# NXGFitTrack API Documentation

## 📡 API ENDPOINTS

Below is the full list of endpoints based entirely on the project code.

---

## 🔐 AUTH ROUTES — `/auth`

- **POST /auth/signup**  
  Register new user  
  **Body:** UserCreate (email, password)  
  **Returns:** UserResponse

- **POST /auth/token**  
  Login and get JWT token  
  **Uses:** OAuth2PasswordRequestForm

---

## 👤 USER ROUTES — `/users`

- **GET /users/me**  
  Get logged-in user  
  **Auth required:** ✔

- **GET /users/me/profile**  
  Get profile of logged-in user  

- **POST /users/me/profile**  
  Create/update user profile  
  **Checks:** payload.user_id == current_user.id

---

## 💪 WORKOUT TEMPLATE ROUTES — `/workouts`

### Templates

- **POST /workouts/templates**  
  Create workout template  
  **Validates:** user_id

- **GET /workouts/templates**  
  List all templates for current user

- **PUT /workouts/templates/{template_id}**  
  Update existing workout template

- **DELETE /workouts/templates/{template_id}**  
  Delete template

### Template Exercises

- **POST /workouts/templates/{template_id}/exercises**  
  Add new exercise to template

- **GET /workouts/templates/{template_id}/exercises**  
  List exercises in template

- **PUT /workouts/exercises/{exercise_id}**  
  Update exercise (name, sets, reps, weight, notes)

- **DELETE /workouts/exercises/{exercise_id}**  
  Delete exercise from template

---

## 📜 HISTORY ROUTES — `/history`

- **POST /history/complete**  
  Record completed workout  
  **Validates:** payload.user_id == current_user.id

- **GET /history/**  
  List completed workout history

- **DELETE /history/all**  
  Delete all history for current user  
  **Returns:** `{ deleted_count }`

---
## 🧪 Testing (Optional)

- Use `pytest`

---

## 📦 Deployment (Production)

Run the app with:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Recommended reverse proxies:  
- Nginx  
- Caddy  
- Docker
