---

# 🧓 Senior Companion Web Application

A comprehensive, full-stack web application designed to empower senior citizens by combating isolation and simplifying daily management. It provides a secure, accessible platform for social connection, health management, cognitive stimulation, and personalized resource discovery.

This project has evolved from a simple content manager into an advanced, real-time, AI‑enhanced platform with background task processing, games, and a built‑in smart assistant.

---

## 🌟 Key Features

### **1. Advanced User System**
- **Dual Roles:** Seniors (simple UI) and Staff (content management dashboard)
- **Secure Authentication:** Standard login/registration
- **Personalized Profiles:** Seniors can set hobbies, emergency contacts, and home location for localized services

---

### **2. Social Connection**
- **Companions System:** Add/remove other seniors as companions  
- **Real-Time Chat:** Private 1‑on‑1 chat using Django Channels + WebSockets

---

### **3. Health & Safety**
- **Medication Reminders:** Automated email reminders using Celery + Redis  
- **Emergency Hospital Finder:** Google Maps integration to locate 24/7 hospitals near the user  
- **Doctor Directory:** Detailed doctor profiles with specialties, languages, and hospital affiliations

---

### **4. Insurance Hub with AI**
- **Policy Management:** Seniors can upload and track insurance policies  
- **Expiry Alerts:** Daily Celery task checks for upcoming expiries  
- **AI Recommendations:**  
  A Machine Learning (Random Forest) model analyzes:
  - Age  
  - Income  
  - Risk tolerance  
  - Health factors  
  …and recommends the best insurance tier and policy plan.

---

### **5. Cognitive Engagement (Games)**
- **Curated Game Library:** Designed for mental stimulation  
- **Memory Match:** High‑contrast, senior‑friendly memory card game  
- **Classic Chess:** Play against a computer opponent  
- **Progress Tracking:** Tracks wins, losses, and sessions

---

### **6. Learning & Resources**
- **Resource Library:** Articles, videos, and tutorials on Tech, Health, Hobbies  
- **Progress Tracking:** Mark resources as *In Progress*, *Completed*, or *Bookmarked*  
- **Places to Visit:** Senior‑friendly directory of parks, museums, clubs with accessibility info

---

### **7. Smart Assistant (Chatbot)**
- **Logic‑Based Chatbot:** Helps users navigate the app  
  Examples:
  - “How do I find a doctor?”
  - “Play a game”
  - “Show my insurance policies”
- **Fallback to Admin:** Unanswered queries are stored and forwarded to staff  
- **Rule Seeding:** Initial rules loaded via `seed_chatbot_rules` command

---

## 🧰 Tech Stack

| Layer | Tools & Libraries |
|-------|-------------------|
| Backend | Django 5.x, Python 3.11 |
| Real-Time | Django Channels, Daphne (ASGI) |
| Async Tasks | Celery, Redis |
| Database | PostgreSQL |
| AI/ML | Scikit-learn, Pandas, Joblib |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Games | Chessboard.js, Chess.js |

---

## 🛠️ Local Development & Setup

### **1. Prerequisites**
- Python 3.11+
- PostgreSQL 12+
- Redis 5.0+  
  *(Windows users: install Redis 5.0.14.1 MSI)*
  Windows Note: Use the Redis 5.0.14.1 MSI installer for compatibility. "https://github.com/tporadowski/redis/releases/tag/v5.0.14.1"

---

### **2. Clone the Repository**

```bash
git clone https://github.com/your-username/senior-companion.git
cd senior-companion
```

---

### **3. Set Up the Environment**

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

### **4. Configuration**

Create a `.env` file:

```env
DB_NAME=senior_companion_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

✅ **ML Model:**  
Place `rf_pipeline.joblib` inside the `ml_models/` folder.

---

### **5. Database Initialization**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_chatbot_rules   # NEW
```

---

### **6. Celery Beat Setup (One-Time)**

In `/admin/` → **DJANGO_CELERY_BEAT**:

| Task | Interval |
|------|----------|
| `reminders.tasks.check_reminders` | Every 60 seconds |
| `reminders.tasks.check_insurance_expiries` | Every 1 day |

---

## ▶️ How to Run (4-Terminal Setup)

### **Terminal 1 — Redis**
```bash
redis-server --port 6380
```

### **Terminal 2 — Django Server**
```bash
python manage.py runserver
```

### **Terminal 3 — Celery Worker**
```bash
celery -A senior_companion_project worker -l INFO -P threads
```

### **Terminal 4 — Celery Beat**
```bash
celery -A senior_companion_project beat -l INFO
```

Access the app at:  
**http://127.0.0.1:8000/**

---

## 📂 Project Structure

```
senior_companion_project/   # Main settings
users/                      # Auth, Profiles, Companions
resources/                  # Hospitals, Insurance, Places, Learning, Games, ML logic
chat/                       # WebSocket chat (Channels)
reminders/                  # Celery tasks for medication & insurance
chatbot/                    # Rule-based smart assistant
templates/                  # Global templates
ml_models/                  # Trained ML models
```

---
