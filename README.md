# SmartTasker

**SmartTasker** is a Django based productivity app that helps you manage daily work using the Pomodoro technique. It organizes tasks, tracks time and provides summaries so you can stay focused and analyze your productivity.

## Features
- **Tasks app**
  - Add, edit and delete tasks
  - Mark tasks as complete
  - Categorize tasks with custom tags
- **Timer app**
  - Pomodoro style timers for each task
  - Start, pause and stop timers
  - Record the time spent on every task
- **Dashboard app**
  - Daily and weekly productivity summaries
  - Compare estimated versus actual time
  - Charts to visualize progress
- **Account app**
  - User registration, login and logout
  - Keeps all task, timer and summary data scoped to each user

## Technologies
- **Language & Framework**: Python (Django)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **Version control**: Git

## Getting Started
1. Clone the repository
   ```bash
   git clone <repo-url>
   cd SmartTasker
   ```
2. Create and activate a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment file and adjust settings
   ```bash
   cp .env.example .env
   # edit .env with your secret key
   ```
5. Apply database migrations
   ```bash
   python manage.py migrate
   ```
6. (Optional) create a superuser for admin access
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server
   ```bash
   python manage.py runserver
   ```
8. Visit `http://127.0.0.1:8000/` in your browser.

## Running Tests
```bash
python manage.py test
```

## Team Members
- Diana Balteanu
- Kaya Sude
- Luke Free
- Alex Kagansky
- Chandler Davis

