# 🧼 Cleaning Schedule App

A simple yet powerful **CRUD web application** built with **Django** that helps shared homes efficiently manage and rotate cleaning tasks.

🧭 Links:
[**App**](https://kingleo.pythonanywhere.com/solo1/)

---

## 🧩 Overview

The **Cleaning Schedule App** allows users to:

- 📝 Create, view, update, and delete cleaning tasks  
- 👥 Assign tasks to house members  
- 📅 Track progress and completed work in real time  

Built with Django’s robust backend, it provides a clean, user-friendly interface for smooth task management — no more paper schedules or whiteboard magnets.

---

## 🌱 Background

When living in Japan, I stayed in a share house where cleaning duties rotated weekly — manually.  
Paper schedules, magnets, and constant reminders… not the most efficient system.

So, I built this app to automate that process — turning household chaos into clean code.

> “Previously: paper and magnets.  
> Now: clicks and automation.”

---

## 🎯 Goals

- Build a simple, intuitive CRUD web app  
- Apply Django models, templates, and views effectively  
- Streamline task management for multiple users  

---

## 🧠 Challenges

- Ensuring smooth CRUD operations with instant feedback  
- Designing a minimal yet functional interface  
- Managing user data and multiple rotating schedules cleanly  

---

## ⚙️ Features

✅ Create, view, update, and delete cleaning tasks  
✅ Assign tasks to users or days  
✅ Track progress and completion in real time  
✅ Mobile-friendly and responsive layout  

---

## 🎓 Learning Outcomes

- Strengthened understanding of **Django architecture (MVT pattern)**  
- Improved skills in **backend logic, ORM, and templates**  
- Practiced designing **user-centered interfaces**  

---

## 🚀 Future Improvements

- 🔁 Auto-rotate weekly tasks  
- 🧍 Remove tenants dynamically when they move out  
- 🏠 Swap tasks between rooms easily  
- 🧹 Add streak tracking for completed chores  
- 🔐 Implement user logins and role permissions  

---

## 🧱 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Django (Python) |
| **Database** | PostgreSQL |
| **Frontend** | HTML · CSS · Django Templates |
| **Version Control** | Git & GitHub |

---

## ⚡ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/cleaning-schedule-app.git
cd cleaning-schedule-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver


python manage.py runserver
```

Visit http://127.0.0.1:8000/
to view the app.
