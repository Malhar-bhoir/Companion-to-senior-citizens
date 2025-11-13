# Companion-to-senior-citizens



# 🧓 Senior Companion Web Application

A comprehensive, database-driven web application built with Django, designed to combat loneliness and isolation among senior citizens. This platform provides a secure environment for social interaction, access to community resources, personalized content, and automated health reminders.

This project was built from the ground up, scaling from a simple content manager to an advanced, real-time application with background task processing.

---

## 🚀 Core Features

- **Dual User System**  
  Separate authentication and permissions for regular Seniors and content-managing Staff.

- **Custom Staff Dashboard**  
  A secure, minimalistic admin panel (separate from Django `/admin`) for staff to manage site content.

- **Content Management System (CMS)**  
  Full CRUD for:
  - Places to Visit
  - Learning Resources
  - Hospitals & Doctors
  - Insurance Policies

- **Personalized Homepage**  
  Dynamically populated with events and resources based on user-selected hobbies.

- **"Companions" Social System**  
  A friends list feature allowing users to add/remove other seniors.

- **Real-Time 1-on-1 Chat**  
  Private chat rooms for companions using Django Channels and WebSockets.

- **Automated Medication Reminders**  
  Background task system using Celery and Redis. Users can schedule multiple reminders. Celery Beat checks every minute and sends real email notifications via SMTP.

---

## 🧰 Tech Stack

| Layer            | Tools & Libraries                                   |
|------------------|-----------------------------------------------------|
| Backend          | Django, Django Channels, Celery                     |
| Database         | PostgreSQL                                          |
| Message Broker   | Redis                                               |
| ASGI Server      | Daphne                                              |
| Frontend         | HTML5, CSS3, Bootstrap 5                            |
| Python Packages  | `psycopg2-binary`, `python-dotenv`                  |

---

## 🛠️ Local Development & Setup

### 1. Prerequisites

You must have the following software installed on your machine:

Python (v3.11+)

PostgreSQL (v12+): The main application database.

Redis (v5.0+): The message broker.

Windows Note: Use the Redis 5.0.14.1 MSI installer for compatibility. "https://github.com/tporadowski/redis/releases/tag/v5.0.14.1"

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/senior-companion.git
cd senior-companion
```

---

### 3. Set Up the Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

---

### 4. Set Up the Database

- Open pgAdmin 4 (or any SQL tool)
- Create a new PostgreSQL database named `senior_companion_db`
- Create a `.env` file in the project root and add:

```env
# --- .env file ---
DB_NAME=senior_companion_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_digit_app_password
```

---

### 5. Initialize the Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### 6. One-Time Manual Setup (Celery Beat)

1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Log in to the admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

3. Scroll to **DJANGO_CELERY_BEAT** → Add a new **Periodic Task**:
   - **Name**: Check Reminders Every Minute
   - **Task**: `reminders.tasks.check_reminders`
   - **Interval**: Add new → Every: `60`, Period: `Seconds`

---

## 🧪 How to Run the Application

This project requires **4 terminals**:

### Terminal 1: Redis Server

```bash
redis-server --port 6380
```

### Terminal 2: Django (Daphne) Server

```bash
.\venv\Scripts\activate
cd senior_companion
python manage.py runserver
```

### Terminal 3: Celery Worker

```bash
.\venv\Scripts\activate
cd senior_companion
celery -A senior_companion_project worker -l INFO -P threads
```

### Terminal 4: Celery Beat

```bash
.\venv\Scripts\activate
cd senior_companion
celery -A senior_companion_project beat -l INFO
```

---

## 🌐 Access the App

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Application Usage

- **Create Content**: Log in as superuser (`/admin/`) → Create Hobby objects  
  Log in as Staff (`/dashboard/`) → Add Events, Places, etc.

- **Test as Senior**: Register a normal user account

- **Set Hobbies**: Go to "My Profile" → Select hobbies

- **Test Personalization**: Homepage updates based on hobbies

- **Test Social**: Register second senior → Add as Companion

- **Test Chat**: Open two browsers → Chat via "Companions"

- **Test Reminders**: Add a medication → Set reminder for 2–3 minutes later  
  → Watch Terminal 3 logs and check your email inbox

