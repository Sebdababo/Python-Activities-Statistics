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
        self.master.title("Daily Activity Tracker")
        self.master.geometry("700x500")
        self.master.configure(bg='#f0f0f0')
        
        self.activities = self.load_activities()
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)
        
        self.activity_entry = ttk.Entry(entry_frame, width=40, font=('Arial', 12))
        self.activity_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.add_button = ttk.Button(entry_frame, text="Add Activity", command=self.add_activity)
        self.add_button.pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.activity_listbox = tk.Listbox(list_frame, width=50, font=('Arial', 10))
        self.activity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.activity_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.activity_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_activity_list()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.stats_button = ttk.Button(button_frame, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_activities)
        self.clear_button.pack(side=tk.LEFT)
        
    def add_activity(self, event=None):
        activity = self.activity_entry.get().strip()
        if activity:
            date = datetime.date.today().strftime("%Y-%m-%d")
            self.activities.setdefault(date, []).append(activity)
            self.update_activity_list()
            self.activity_entry.delete(0, tk.END)
            self.save_activities()
        else:
            messagebox.showwarning("Warning", "Please enter an activity.")
    
    def update_activity_list(self):
        self.activity_listbox.delete(0, tk.END)
        for date, activities in sorted(self.activities.items(), reverse=True):
            for activity in activities:
                self.activity_listbox.insert(tk.END, f"{date}: {activity}")
    
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
            self.save_activities()
    
    def save_activities(self):
        with open('activities.json', 'w') as f:
            json.dump(self.activities, f)
    
    def load_activities(self):
        try:
            with open('activities.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityTracker(root)
    root.mainloop()