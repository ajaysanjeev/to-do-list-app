import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import time
from plyer import notification
import datetime
import matplotlib.pyplot as plt
import os
import tkinter.messagebox

# ✅ Create the Tkinter root window FIRST
root = tk.Tk()
root.title("Smart To-Do List App")
root.geometry("900x600")  # Resize window

# ✅ Define Correct Background Image Path
bg_image_path = r"C:\Users\AKSHAYA\ToDoApp\def.jpeg"  # Make sure this file exists

# ✅ Load Background Image AFTER Creating Tkinter Window
try:
    bg_image = Image.open(bg_image_path).resize((900, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("❌ Background image not found! Please check the file location.")

# ✅ Delete and Recreate Database to Fix `entry_date` Issue
if os.path.exists("tasks.db"):
    os.remove("tasks.db")  # Delete old database to fix missing column
    print("✅ Old database deleted. A new one will be created!")

# ✅ Initialize Database for Tracking Entries
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    task TEXT,
    completed BOOLEAN,
    entry_date TEXT
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY,
    date TEXT
)""")
conn.commit()
conn.close()
print("✅ New database created successfully!")

# Function to Show Badge Pop-up with Star Image
# Function to Show Badge Pop-up with Star Image & Motivational Message
# ✅ Updated function to center pop-up window correctly
def show_badge_popup(badge_text):
    popup = tk.Toplevel(root)  # Create pop-up window
    popup.title("🏆 Badge Earned!")
    popup.geometry("400x300")  # Set window size

    # ✅ Center the window manually
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f"+{x}+{y}")

    # Load star image
    try:
        star_img = Image.open("star.png").resize((100, 100))
        star_photo = ImageTk.PhotoImage(star_img)
        star_label = tk.Label(popup, image=star_photo)
        star_label.image = star_photo
        star_label.pack(pady=10)
    except FileNotFoundError:
        print("❌ Star image not found!")

    # ✅ Display badge message & motivational quote
    msg_label = tk.Label(popup, text=badge_text + "\n\nDon't lose your hope, move on!", font=("Arial", 14, "bold"), fg="black", justify="center")
    msg_label.pack(pady=10)

    # Close Button
    close_button = tk.Button(popup, text="OK", command=popup.destroy, width=10)
    close_button.pack(pady=10)

# Attractive Welcome Message
welcome_label = tk.Label(root, text="✨ Welcome to Your To-Do List! ✨", 
                         font=("Rubik", 24, " bold"), fg="black", bg="white")
welcome_label.pack(pady=10)

# Task Entry Box with Padding
task_entry = tk.Text(root, width=40,height=1, font=("Times New Roman", 20, "bold"), bg="white", fg="black")
task_entry.pack(pady=5)

# Left-Side Command Panel
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, padx=10)

task_list_frame = tk.Frame(root)
task_list_frame.pack(pady=10)

# Store Task Checkboxes
task_checkboxes = []

# Function to Add Task
def add_task():
    task = task_entry.get("1.0", tk.END).strip()
    if task:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(task_list_frame, text=task, variable=var, font=("Times New Roman", 20, "bold"))
        checkbox.pack(anchor="w")

        # ✅ Store actual widget reference in the list (instead of text)
        task_checkboxes.append((checkbox, var))

        save_task_to_db(task)
        task_entry.delete("1.0", tk.END)  # ✅ Clears input box


def delete_task():
    for checkbox, var in task_checkboxes[:]:  # ✅ Iterate safely using a copy
        if var.get():  # ✅ Check if checkbox is selected
            checkbox.destroy()  # ✅ Remove checkbox widget from UI
            task_checkboxes.remove((checkbox, var))  # ✅ Remove task from list
def save_task_to_db(task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, completed, entry_date) VALUES (?, ?, ?)",
                   (task, False, str(datetime.date.today())))
    conn.commit()
    conn.close()

# Badge System Based on Daily Entries
def calculate_badge():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT entry_date) FROM tasks")
    days = cursor.fetchone()[0]
    conn.close()

    if days >= 30:
        return "🏆 Gold Star! You've been consistent for 30 days!"
    elif days >= 15:
        return "🥈 Silver Star! Keep up the great work!"
    elif days >= 3:
        return "🥉 Bronze Star! You're off to a great start!"
    else:
        return "Keep adding tasks daily to earn badges!"

# Function to Notify User Daily
def send_reminder():
    notification.notify(
        title="Task Reminder!",
        message="You have tasks to complete today!",
        timeout=10
    )

# Function to Track Daily Progress
def update_daily_tracking():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    today = str(datetime.date.today())
    cursor.execute("SELECT * FROM user_progress WHERE date = ?", (today,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO user_progress (date) VALUES (?)", (today,))
    conn.commit()
    conn.close()

# Weekly & Monthly Progress Visualization
def show_report():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT entry_date) FROM tasks")
    days_completed = cursor.fetchone()[0]
    conn.close()

    plt.bar(["Weekly Progress", "Monthly Progress"], [days_completed // 7, days_completed])
    plt.title("Task Completion Report")
    plt.show()

# Add Buttons
add_button = tk.Button(button_frame, text="➕ Add Task", command=add_task, width=15,height=2, font=("Times New Roman", 12, "bold"),bg="black",fg="white")
add_button.pack(pady=5)

delete_button = tk.Button(button_frame, text="❌ Delete Task", command=delete_task, width=15)
delete_button.pack(pady=5)

reminder_button = tk.Button(button_frame, text="🔔 Send Reminder", command=send_reminder, width=15)
reminder_button.pack(pady=5)

report_button = tk.Button(button_frame, text="📊 Show Report", command=show_report, width=15)
report_button.pack(pady=5)

# ✅ Updated Badge Button to Show Pop-up with Star Image
badge_button = tk.Button(button_frame, text="🏆 Show Badge", command=lambda: show_badge_popup("🏆 No badge yet! Keep adding tasks daily!"), width=15)
badge_button.pack(pady=5)

# Run Daily Tracking
update_daily_tracking()

# Run the GUI Loop
root.mainloop()