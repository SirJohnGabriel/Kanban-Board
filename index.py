import tkinter as tk
import sqlite3
from tkinter import messagebox
from customtkinter import *

from initdb import init_db

class KanbanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanban Board")
        root.configure(bg='#212529')

        root.iconbitmap('assets/Kanban_App_Logo.ico')

        window_width = 600
        window_height = 400

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        main_frame = CTkScrollableFrame(root, fg_color="#212529")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.todo_frame = CTkFrame(main_frame, fg_color="#212529")
        self.inprogress_frame = CTkFrame(main_frame, fg_color="#212529")
        self.done_frame = CTkFrame(main_frame, fg_color="#212529")

        self.todo_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand =  True)
        self.inprogress_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand =  True)
        self.done_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand =  True)

        CTkLabel(self.todo_frame, text="To-Do", fg_color="#212529").pack(fill = "x")
        CTkLabel(self.inprogress_frame, text="Doing", fg_color="#212529").pack(fill = "x")
        CTkLabel(self.done_frame, text="Done", fg_color="#212529").pack(fill = "x")

        CTkButton(self.root, text="Add Task", command=self.add_task, fg_color="#f8f9fa", text_color="#000000").pack(pady=10)

        self.load_tasks()
    
    def load_tasks(self):
        conn = sqlite3.connect('kanban.db')
        c = conn.cursor()
        c.execute("SELECT id, title, description, status FROM tasks")
        tasks = c.fetchall()
        conn.close()

        for widget in self.todo_frame.winfo_children()[1:]:
            widget.destroy()
        for widget in self.inprogress_frame.winfo_children()[1:]:
            widget.destroy()
        for widget in self.done_frame.winfo_children()[1:]:
            widget.destroy()

        for task in tasks:
            self.add_task_to_column(task)

    def add_task_to_column(self, task):
        task_id, title, description, status = task
        task_frame = CTkFrame(self.todo_frame if status == 'To-Do' else self.inprogress_frame if status == 'In-Progress' else self.done_frame, fg_color="#343a40")
        CTkLabel(task_frame, text=title).pack(fill='x', anchor='w', padx = 5, pady = 5)
        CTkLabel(task_frame, text=description).pack(fill='x', anchor='w', padx = 5, pady = 5)
        status_button_text = "Doing" if status == "To-Do" else "Done" if status == "In-Progress" else "To-Do"
        CTkButton(task_frame, text=status_button_text, command=lambda t=task: self.change_status(t)).pack(padx = 0, pady = 0, fill = "x")
        CTkButton(task_frame, text="Edit", command=lambda t=task: self.edit_task(t)).pack(padx = 0, pady = 5, fill = "x")
        CTkButton(task_frame, text="Delete", command=lambda t=task: self.delete_task(t)).pack(padx = 0, pady = 0, fill = "x")
        task_frame.pack(pady=5, fill=tk.BOTH, expand=True)

    def add_task(self):
        self.new_task_window = tk.Toplevel(self.root)
        self.new_task_window.title("Add Task")

        self.new_task_window.configure(bg="#212529")
        self.new_task_window.iconbitmap('assets/Kanban_App_Logo.ico')

        window_width = 300
        window_height = 300

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.new_task_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        CTkLabel(self.new_task_window, text="Title", text_color="#FFFFFF", bg_color="#212529").pack(padx = 5, pady = 5)
        self.title_entry = CTkEntry(self.new_task_window)
        self.title_entry.pack()

        CTkLabel(self.new_task_window, text="Description", text_color="#FFFFFF", bg_color="#212529").pack(padx = 5, pady = 5)
        self.desc_entry = CTkEntry(self.new_task_window)
        self.desc_entry.pack()

        CTkButton(self.new_task_window, text="Add", command=self.save_task).pack(pady = (10, 0))

    def save_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        status = "To-Do"

        conn = sqlite3.connect('kanban.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, description, status))
        conn.commit()
        conn.close()

        self.new_task_window.destroy()
        self.load_tasks()

    def edit_task(self, task):
        task_id, title, description, status = task

        self.edit_task_window = tk.Toplevel(self.root)
        self.edit_task_window.title("Edit Task")

        tk.Label(self.edit_task_window, text="Title").pack()
        self.edit_title_entry = tk.Entry(self.edit_task_window)
        self.edit_title_entry.insert(0, title)
        self.edit_title_entry.pack()

        tk.Label(self.edit_task_window, text="Description").pack()
        self.edit_desc_entry = tk.Entry(self.edit_task_window)
        self.edit_desc_entry.insert(0, description)
        self.edit_desc_entry.pack()

        tk.Button(self.edit_task_window, text="Save", command=lambda: self.save_edited_task(task_id)).pack()

    def save_edited_task(self, task_id):
        title = self.edit_title_entry.get()
        description = self.edit_desc_entry.get()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        conn = sqlite3.connect('kanban.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ?", (title, description, task_id))
        conn.commit()
        conn.close()

        self.edit_task_window.destroy()
        self.load_tasks()

    def change_status(self, task):
        task_id, title, description, status = task

        new_status = "In-Progress" if status == "To-Do" else "Done" if status == "In-Progress" else "To-Do"

        conn = sqlite3.connect('kanban.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        conn.close()

        self.load_tasks()

    def delete_task(self, task):
        task_id = task[0]
        conn = sqlite3.connect('kanban.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = KanbanApp(root)
    root.mainloop()
