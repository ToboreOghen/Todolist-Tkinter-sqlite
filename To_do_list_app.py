import tkinter as tk
from tkinter import messagebox, END, ANCHOR
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("tasks.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS tasks (
            task TEXT
        )""")
conn.commit()


# --- Functions ---
def load_tasks():
    listbox.delete(0, tk.END)
    c.execute("SELECT task FROM tasks")
    for row in c.fetchall():
        listbox.insert(tk.END, row[0])


def add_task():
    task = task_entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        c.execute("INSERT INTO tasks VALUES (?)", (task,))
        conn.commit()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")


def delete_task():
    try:
        selected_task = listbox.get(ANCHOR)
        listbox.delete(ANCHOR)
        c.execute("DELETE FROM tasks WHERE task = ?", (selected_task,))
        conn.commit()
    except:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")


def clear_tasks():
    listbox.delete(0, tk.END)
    c.execute("DELETE FROM tasks")
    conn.commit()


def edit_task():
    try:
        selected_index = listbox.curselection()[0]
        old_task = listbox.get(selected_index)
        new_task = task_entry.get()
        if new_task.strip() == "":
            messagebox.showwarning("Input Error", "Please enter a new task.")
            return
        # Update Listbox
        listbox.delete(selected_index)
        listbox.insert(selected_index, new_task)
        # Update DB
        c.execute("UPDATE tasks SET task = ? WHERE task = ?", (new_task, old_task))
        conn.commit()
        task_entry.delete(0, tk.END)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")


def exit_app():
    conn.close()
    root.destroy()


# --- Main Window ---
root = tk.Tk()
root.title("To-Do List")
root.geometry("480x520")
root.config(bg="lightblue")

# --- Title ---
title_label = tk.Label(root, text="To Do List.", 
                       font=("Brush Script MT", 18, "bold"),
                       bg="lightblue", fg="darkblue")
title_label.pack(pady=10)

# --- Entry box (top) ---
task_entry = tk.Entry(root, font=("Brush Script MT", 16, "italic"), width=30, bd=0)
task_entry.pack(pady=8)

# ✅ Fix: Ensure keyboard shows when clicking entry on Android
def refocus_entry(event):
    root.after(100, lambda: task_entry.focus_set())

task_entry.bind("<Button-1>", refocus_entry)

# --- Frame for Listbox + Scrollbar ---
frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=15)

# Scrollbar
my_scrollbar = tk.Scrollbar(frame)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox
listbox = tk.Listbox(
    frame,
    width=35,
    height=10,
    font=("Brush Script MT", 16, "italic"),
    bd=0,
    fg="#333333",
    bg="white",
    selectbackground="skyblue",
    activestyle="none"
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Connect Scrollbar to Listbox
listbox.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=listbox.yview)

# --- Button Frame (bottom) ---
button_frame = tk.Frame(root, bg="lightblue")
button_frame.pack(pady=15)

# Buttons (all in one row, resized)
add_button = tk.Button(button_frame, text="Add", width=9, command=add_task, bd=0, font=("Brush Script MT", 14))
add_button.grid(row=0, column=0, padx=4, pady=5)

edit_button = tk.Button(button_frame, text="Edit", width=9, command=edit_task, bd=0, font=("Brush Script MT", 14))
edit_button.grid(row=0, column=1, padx=4, pady=5)

delete_button = tk.Button(button_frame, text="Delete", width=9, command=delete_task, bd=0, font=("Brush Script MT", 14))
delete_button.grid(row=1, column=0, padx=4, pady=5)

clear_button = tk.Button(button_frame, text="Clear", width=9, command=clear_tasks, bd=0, font=("Brush Script MT", 14))
clear_button.grid(row=1, column=1, padx=4, pady=5)

exit_button = tk.Button(button_frame, text="Exit", width=9, command=exit_app, bd=0, font=("Brush Script MT", 14))
exit_button.grid(row=2, column=0, padx=4, pady=5)

# --- Load tasks from DB at start ---
load_tasks()

# --- Run the app ---
root.mainloop()