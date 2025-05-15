# to-do-list-app
To do list app
🧠 Smart To-Do List App (Tkinter + SQLite + Plyer)
A visually appealing and feature-rich To-Do List application built using Python’s tkinter GUI library. The app motivates users with badges, sends daily reminders, and tracks task completion progress with reports.

Features
✅ Add, delete, and track tasks with checkboxes
🏆 Badge system based on daily consistency (Bronze, Silver, Gold)
📅 Progress tracking and visualization (Weekly & Monthly)
🔔 Desktop notifications using plyer
📊 Local storage using SQLite database
🎨 Custom background image and UI design
🌟 Pop-up badges with motivational quotes and star images
📸 Screenshot
(https://github.com/user-attachments/assets/fdc2f2e3-f2de-48dd-90e9-88d207b7c47e)

🛠 Installation
Clone the Repository
Install Required Libraries

bash Copy Edit pip install pillow plyer matplotlib Run the App

bash Copy Edit python todo_app.py Project Structure python Copy Edit todo-app/ │ ├── todo_app.py # Main application code ├── def.jpeg # Background image ├── star.png # Star image used for badge pop-ups ├── tasks.db # SQLite database (auto-generated) └── README.md # Project info Requirements Python 3.10+

tkinter (comes with standard Python)

Pillow for image processing

plyer for notifications

matplotlib for report plotting

Badge Criteria 🥉 Bronze: 3 days of task entries

🥈 Silver: 15 days of task entries

🏆 Gold: 30+ days of consistency
