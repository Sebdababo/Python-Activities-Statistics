import tkinter as tk
from tkinter import ttk, messagebox
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
        self.master.configure(bg='#f0f0f0')
        
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
        
        self.activity_entry = ttk.Entry(entry_frame, width=40, font=('Arial', 12))
        self.activity_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.activity_entry.bind('<Return>', self.add_activity)
        
        self.add_button = ttk.Button(entry_frame, text="Add Activity", command=self.add_activity)
        self.add_button.pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.activity_listbox = tk.Listbox(list_frame, width=50, font=('Arial', 10))
        self.activity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.activity_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.activity_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_activity_list()
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.stats_button = ttk.Button(button_frame, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear All Activities", command=self.clear_activities)
        self.clear_button.pack(side=tk.LEFT)

    def create_todo_widgets(self, parent):
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(fill=tk.X, pady=10)
        
        self.todo_entry = ttk.Entry(entry_frame, width=40, font=('Arial', 12))
        self.todo_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.todo_entry.bind('<Return>', self.add_todo)
        
        self.add_todo_button = ttk.Button(entry_frame, text="Add Task", command=self.add_todo)
        self.add_todo_button.pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.todo_listbox = tk.Listbox(list_frame, width=50, font=('Arial', 10))
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.todo_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.todo_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_todo_list()
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.complete_button = ttk.Button(button_frame, text="Mark as Complete", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.remove_button = ttk.Button(button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT)

    def add_activity(self, event=None):
        activity = self.activity_entry.get().strip()
        if activity:
            date = datetime.date.today().strftime("%Y-%m-%d")
            self.activities.setdefault(date, []).append(activity)
            self.update_activity_list()
            self.activity_entry.delete(0, tk.END)
            self.save_data('activities.json', self.activities)
        else:
            messagebox.showwarning("Warning", "Please enter an activity.")
    
    def update_activity_list(self):
        self.activity_listbox.delete(0, tk.END)
        for date, activities in sorted(self.activities.items(), reverse=True):
            for activity in activities:
                self.activity_listbox.insert(tk.END, f"{date}: {activity}")
    
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
        stats_window.geometry("800x600")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        dates = list(self.activities.keys())
        activity_counts = [len(activities) for activities in self.activities.values()]
        
        ax1.bar(dates, activity_counts, color='skyblue')
        ax1.set_title("Activities per Day", fontsize=14)
        ax1.set_xlabel("Date", fontsize=12)
        ax1.set_ylabel("Number of Activities", fontsize=12)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        all_activities = [activity for activities in self.activities.values() for activity in activities]
        top_activities = Counter(all_activities).most_common(5)
        activity_names, activity_counts = zip(*top_activities)
        
        ax2.bar(activity_names, activity_counts, color='lightgreen')
        ax2.set_title("Top 5 Most Common Activities", fontsize=14)
        ax2.set_xlabel("Activity", fontsize=12)
        ax2.set_ylabel("Frequency", fontsize=12)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    def clear_activities(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all activities?"):
            self.activities.clear()
            self.update_activity_list()
            self.save_data('activities.json', self.activities)
    
    def save_data(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} if filename == 'activities.json' else []

if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityTracker(root)
    root.mainloop()