# BlogForge

A functional Django blog app with authentication, CRUD post management, and a dynamic sidebar.

## Features
- Register, login, logout
- Create, read, update, and delete blog posts
- Latest posts and quick links in the sidebar
- Bootstrap-based UI

## Run
1. Create and activate a Python 3.9 virtual environment
2. Install Django 3.0.11
3. Run migrations
4. Start the server

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install django==3.0.11
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.
