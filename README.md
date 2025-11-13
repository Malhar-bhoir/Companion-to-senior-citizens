# Companion-to-senior-citizens

Senior Companion Web ApplicationA comprehensive, database-driven web application built with Django, designed to combat loneliness and isolation among senior citizens. This platform provides a secure environment for social interaction, access to community resources, personalized content, and automated health reminders.This project was built from the ground up, scaling from a simple content manager to an advanced, real-time application with background task processing.Core FeaturesDual User System: Separate authentication and permissions for regular Seniors and content-managing Staff.Custom Staff Dashboard: A secure, "minimalistic" admin panel (separate from the main Django /admin) for staff to easily add and manage site content.Content Management System: A full CRUD system for:Places to VisitLearning ResourcesHospitals & DoctorsInsurance PoliciesPersonalized Homepage: The user's homepage is dynamically populated with events and learning resources based on their self-selected Hobbies."Companions" Social System: A "friends list" feature allowing users to add and remove other seniors from their personal companion list.Real-Time 1-on-1 Chat: A private, real-time chat room for users who are companions, built with Django Channels and WebSockets.Automated Medication Reminders: A robust background task system using Celery and Redis. Users can add medications and set multiple reminder times. A Celery "Beat" (scheduler) checks every minute and sends real email reminders via SMTP.Tech StackBackend: Django, Django Channels (for WebSockets), Celery (for background tasks)Database: PostgreSQL (production-ready and thread-safe)Message Broker & Cache: Redis (powers both Celery and Channels)ASGI Server: DaphneFrontend: HTML5, CSS3, Bootstrap 5Python Libraries: psycopg2-binary (PostgreSQL connector), python-dotenv (for security)Local Development & SetupThis is an advanced application that requires multiple services to run.1. PrerequisitesYou must have the following software installed on your machine:Python (v3.11+)PostgreSQL (v12+): The main application database.Redis (v5.0+): The message broker.Windows Note: Use the Redis 5.0.14.1 MSI installer for compatibility.2. Clone the Repositorygit clone [https://github.com/your-username/senior-companion.git](https://github.com/your-username/senior-companion.git)
cd senior-companion
3. Set Up the Environment# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# Install all required Python packages
pip install -r requirements.txt
4. Set Up the DatabaseOpen pgAdmin 4 (or your preferred SQL tool).Create a new PostgreSQL database. This guide will assume it is named senior_companion_db.Create a new file named .env in the project root (senior_companion/) to hold your secret keys.Copy the contents of .env.example (or the block below) into your new .env file and fill in your database credentials..env file contents:# --- .env file ---

# PostgreSQL Database
# (Change 'your_postgres_password' to the one you set during installation)
DB_NAME=senior_companion_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Gmail SMTP for Email Reminders
# 1. Get a 16-digit "App Password" from your Google Account
# 2. Add your email and that App Password below
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_digit_app_password
5. Initialize the Database# Create all the database tables
python manage.py migrate

# Create your first Superuser account
python manage.py createsuperuser
6. One-Time Manual Setup (Crucial!)For the reminder system to work, you must set its schedule in the admin panel.Start the Django server (python manage.py runserver).Log in to the admin panel at http://127.0.0.1:8000/admin/ with your superuser.Scroll down to the DJANGO_CELERY_BEAT section.Click "Add" next to "Periodic tasks".Fill out the form:Name: Check Reminders Every MinuteTask (registered): Select reminders.tasks.check_remindersInterval: Click +, set Every: 60 and Period: Seconds, then "Save".Click "Save" on the main "Add periodic task" page.How to Run the ApplicationThis project requires 4 separate terminals to run all services.Terminal 1: Redis ServerOpen a terminal and run the Redis server on the correct port.redis-server --port 6380
Terminal 2: Django (Daphne) ServerOpen a second terminal, activate your venv, and run the Django server..\venv\Scripts\activate
cd senior_companion
python manage.py runserver
Terminal 3: Celery WorkerOpen a third terminal, activate your venv, and run the Celery worker. This terminal will show the !!! REMINDER !!! logs and send emails..\venv\Scripts\activate
cd senior_companion
celery -A senior_companion_project worker -l INFO -P threads
Terminal 4: Celery BeatOpen a fourth terminal, activate your venv, and run the Celery beat (scheduler). This terminal will log "Sending due task..." every minute..\venv\Scripts\activate
cd senior_companion
celery -A senior_companion_project beat -l INFO
You can now access the application at http://127.0.0.1:8000/.Application UsageCreate Content: Log in as your superuser (/admin/) and create Hobby objects. Log in as a Staff user (/dashboard/) to add Events, Places, etc.Test as Senior: Register a new, normal user account.Set Hobbies: Go to "My Profile" and select hobbies.Test Personalization: Go back to the Homepage to see personalized content.Test Social: Register a second senior user. Log in as the first user, go to "Companions," and add the second user.Test Chat: Open two browsers (one as each senior user). Go to "Companions" and click "Chat" to open a real-time chat room.Test Reminders: Go to "My Reminders," add a medication, and set a reminder for 2-3 minutes in the future. Watch Terminal 3 (Worker) and check your email inbox.LicenseThis project is licensed under the MIT License.
