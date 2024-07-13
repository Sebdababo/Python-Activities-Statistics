import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from collections import Counter
import json

class ActivityTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Activity Tracker & TO DO List")
        self.master.geometry("800x600")
        
        self.activities = self.load_data('activities.json')
        self.todo_list = self.load_data('todo.json')
        
        self.create_widgets()
        
    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        activities_frame = ttk.Frame(notebook, padding="10")
        notebook.add(activities_frame, text="Activities")
        self.create_activities_widgets(activities_frame)
        
        todo_frame = ttk.Frame(notebook, padding="10")
        notebook.add(todo_frame, text="TO DO List")
        self.create_todo_widgets(todo_frame)
    
    def create_activities_widgets(self, parent):
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(fill=tk.X, pady=10)
        
        self.date_entry = ttk.Entry(entry_frame, width=10, font=('Arial', 14))
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.time_entry = ttk.Entry(entry_frame, width=8, font=('Arial', 14))
        self.time_entry.insert(0, datetime.datetime.now().strftime("%H:%M"))
        self.time_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.activity_entry = ttk.Entry(entry_frame, width=30, font=('Arial', 14))
        self.activity_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.activity_entry.bind('<Return>', self.add_activity)
        
        self.add_button = ttk.Button(entry_frame, text="Add Activity", command=self.add_activity)
        self.add_button.pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.activity_listbox = tk.Listbox(list_frame, width=50, font=('Arial', 12))
        self.activity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.activity_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.activity_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_activity_list()
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.stats_button = ttk.Button(button_frame, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.remove_activity_button = ttk.Button(button_frame, text="Remove Activity", command=self.remove_activity)
        self.remove_activity_button.pack(side=tk.LEFT, padx=(0, 5))

        self.edit_activity_button = ttk.Button(button_frame, text="Edit Activity", command=self.edit_activity)
        self.edit_activity_button.pack(side=tk.LEFT, padx=(0, 5))

        self.remove_all_activities_button = ttk.Button(button_frame, text="Remove All Activities", command=self.remove_all_activities)
        self.remove_all_activities_button.pack(side=tk.LEFT, padx=(0, 5))

    def create_todo_widgets(self, parent):
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(fill=tk.X, pady=10)
        
        self.todo_entry = ttk.Entry(entry_frame, width=40, font=('Arial', 14))
        self.todo_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.todo_entry.bind('<Return>', self.add_todo)
        
        self.add_todo_button = ttk.Button(entry_frame, text="Add Task", command=self.add_todo)
        self.add_todo_button.pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.todo_listbox = tk.Listbox(list_frame, width=50, font=('Arial', 12))
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.todo_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.todo_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_todo_list()
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.complete_button = ttk.Button(button_frame, text="Mark as Complete", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.remove_button = ttk.Button(button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=(0, 5))

        self.edit_task_button = ttk.Button(button_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(side=tk.LEFT, padx=(0, 5))

        self.remove_all_tasks_button = ttk.Button(button_frame, text="Remove All Tasks", command=self.remove_all_tasks)
        self.remove_all_tasks_button.pack(side=tk.LEFT, padx=(0, 5))

    def add_activity(self, event=None):
        activity = self.activity_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        if activity and date and time:
            try:
                datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                date_time = f"{date} {time}"
                self.activities.setdefault(date_time, []).append(activity)
                self.update_activity_list()
                self.activity_entry.delete(0, tk.END)
                self.save_data('activities.json', self.activities)
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
        else:
            messagebox.showwarning("Warning", "Please enter date, time, and activity.")
    
    def update_activity_list(self):
        self.activity_listbox.delete(0, tk.END)
        for date_time, activities in sorted(self.activities.items(), reverse=True):
            for activity in activities:
                self.activity_listbox.insert(tk.END, f"{date_time}: {activity}")
    
    def add_todo(self, event=None):
        task = self.todo_entry.get().strip()
        if task:
            self.todo_list.append({"task": task, "completed": False})
            self.update_todo_list()
            self.todo_entry.delete(0, tk.END)
            self.save_data('todo.json', self.todo_list)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def update_todo_list(self):
        self.todo_listbox.delete(0, tk.END)
        for idx, item in enumerate(self.todo_list):
            status = "✓" if item["completed"] else " "
            self.todo_listbox.insert(tk.END, f"[{status}] {item['task']}")
            if item["completed"]:
                self.todo_listbox.itemconfig(idx, {'fg': 'gray'})
    
    def complete_task(self):
        selection = self.todo_listbox.curselection()
        if selection:
            index = selection[0]
            self.todo_list[index]["completed"] = not self.todo_list[index]["completed"]
            self.update_todo_list()
            self.save_data('todo.json', self.todo_list)
        else:
            messagebox.showinfo("Info", "Please select a task to mark as complete.")
    
    def remove_task(self):
        selection = self.todo_listbox.curselection()
        if selection:
            index = selection[0]
            del self.todo_list[index]
            self.update_todo_list()
            self.save_data('todo.json', self.todo_list)
        else:
            messagebox.showinfo("Info", "Please select a task to remove.")

    def show_statistics(self):
        if not self.activities:
            messagebox.showinfo("Info", "No activities recorded yet.")
            return
        
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Activity Statistics")
        stats_window.geometry("1600x1200")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        dates = list(self.activities.keys())
        activity_counts = [len(activities) for activities in self.activities.values()]
        
        ax1.bar(dates, activity_counts, color='skyblue')
        ax1.set_title("Activities per Day", fontsize=18)
        ax1.set_xlabel("Date", fontsize=16)
        ax1.set_ylabel("Number of Activities", fontsize=16)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        all_activities = [activity for activities in self.activities.values() for activity in activities]
        top_activities = Counter(all_activities).most_common(5)
        activity_names, activity_counts = zip(*top_activities)
        
        ax2.bar(activity_names, activity_counts, color='lightgreen')
        ax2.set_title("Top 5 Most Common Activities", fontsize=18)
        ax2.set_xlabel("Activity", fontsize=16)
        ax2.set_ylabel("Frequency", fontsize=16)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    def save_data(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} if filename == 'activities.json' else []

    def remove_activity(self):
        selection = self.activity_listbox.curselection()
        if selection:
            index = selection[0]
            date_time, activity = self.activity_listbox.get(index).split(': ', 1)
            self.activities[date_time].remove(activity)
            if not self.activities[date_time]:
                del self.activities[date_time]
            self.update_activity_list()
            self.save_data('activities.json', self.activities)
        else:
            messagebox.showinfo("Info", "Please select an activity to remove.")

    def edit_activity(self):
        selection = self.activity_listbox.curselection()
        if selection:
            index = selection[0]
            date_time, old_activity = self.activity_listbox.get(index).split(': ', 1)
            new_activity = simpledialog.askstring("Edit Activity", "Enter new activity:", initialvalue=old_activity)
            if new_activity:
                self.activities[date_time].remove(old_activity)
                self.activities[date_time].append(new_activity)
                self.update_activity_list()
                self.save_data('activities.json', self.activities)
        else:
            messagebox.showinfo("Info", "Please select an activity to edit.")

    def edit_task(self):
        selection = self.todo_listbox.curselection()
        if selection:
            index = selection[0]
            old_task = self.todo_list[index]['task']
            new_task = simpledialog.askstring("Edit Task", "Enter new task:", initialvalue=old_task)
            if new_task:
                self.todo_list[index]['task'] = new_task
                self.update_todo_list()
                self.save_data('todo.json', self.todo_list)
        else:
            messagebox.showinfo("Info", "Please select a task to edit.")

    def remove_all_activities(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to remove all activities?"):
            self.activities.clear()
            self.update_activity_list()
            self.save_data('activities.json', self.activities)

    def remove_all_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to remove all tasks?"):
            self.todo_list.clear()
            self.update_todo_list()
            self.save_data('todo.json', self.todo_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityTracker(root)
    root.mainloop()