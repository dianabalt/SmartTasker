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
   source venv/bin/activate | or | venv/scripts/activate (on windows)
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations
   ```bash
   python manage.py migrate
   ```
5. (Optional) create a superuser for admin access
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server
   ```bash
   python manage.py runserver
   ```
7. Visit `http://127.0.0.1:8000/` in your browser.

## Running Tests
```bash
python manage.py test
```

##HOW TO USE APP

1. Create an Account or Log In
  - Start by registering a new account or logging in with your existing credentials.

2. Add Tasks for Today or This Week
  - To plan tasks for the current day, go to the Daily Tasks page and add tasks using the “Add New Task” button.
  - If you want to plan tasks for any day of the current week, use the Weekly Tasks page. Select the specific day (Monday–Sunday) and add tasks to that day.

3. Plan Ahead or Review Past Tasks
  - To plan for future weeks, click the Next Week button on the Weekly Tasks page. You can add tasks to any day of upcoming weeks.
  - To review or edit tasks from previous weeks, use the Previous Week button.

4. Search and Filter Tasks
  - Use the search bar at the top of the Daily or Weekly Tasks page to quickly find any task by task title (task name).
  - If you use different categories for your tasks, you can filter tasks by category. The filter dropdown only shows categories that actually exist in your current tasks.
  
5. Add and Edit Task Details
- When adding or editing a task, you can set:
   -  Task Title: What the task is called.
   -  Description: Any extra details or notes.
   -  Deadline: When the task must be completed.
   -  Goal Date: (Optional) If you want to finish earlier than the deadline.
   -  Category Name: For grouping or filtering tasks.
   -  Category Color: For visual identification.
   -  Estimated Time: How long you think you’ll spend on the task (set in hours, minutes, and seconds).
   -  You can edit exisitng takss at any point using the edit button
 
6. Start, Pause, and Stop Timers
  - Each task has a Time Remaining timer based on your estimated time.
  - When you’re ready to work, click "Start" button under remaining time to begin the countdown.
  - You can Pause or Stop the timer at any time. Stop resets the timer to your original estimate.
  - When time runs out, you’ll be notified and the Overtime Timer begins, counting how much extra time you spend.

7. Overtime Timer
  - If your estimated time runs out while working, you’ll see a notification: “Time’s up for task: [Task Name]. Click OK to begin overtime timer.”
  -  The Overtime Timer will start counting up. This lets you keep tracking how long you work past your original estimate, if needed.
  -  Both timers are always kept in sync—whether you’re on the Daily, Weekly Tasks page, or the Dashboard

8. Complete Tasks
   - When you finish a task, click the circle icon to the left of the task.
   - Completed tasks will be moved to the “Completed Tasks” section, grayed out, and display a green check mark.

9. View Dashboard and Analytics
  - Go to the Dashboard page to see live stats and visualizations, including:
    -   Total Tasks: Number of tasks this week.
    -   Completed Tasks: Number of tasks finished (shown with a green check mark and grayed out).
    -   Total Estimated Time: The sum of estimated times for all added tasks.
    -   Time Spent Today / This Week: live timers add up time as you work, counting both time left on countdowns and time going up on overtime for all active tasks, so you always see exactly how much time you’re actively spending.
    -   Live Graph: A bar chart showing, for each task, your original estimate (blue) vs. the actual time spent (red), combining time from both countdown and overtime timers.

10. Navigate Easily
    - Use the navigation bar to quickly move between Home, Daily Tasks, Weekly Tasks, Dashboard, and Logout.

TIPS:
- You can edit or delete any task at any time by clicking the corresponding button.
- Timers and overtime are automatically saved and synced in your browser, so you can safely switch between pages without losing your progress.
- Category colors make it easier to visually organize and identify tasks at a glance.



-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Team Members
- Diana Balteanu
- Kaya Sude
- Luke Free
- Alex Kagansky
- Chandler Davis

## License

This project is licensed under the MIT License.
