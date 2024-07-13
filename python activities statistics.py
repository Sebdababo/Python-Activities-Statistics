import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class JobTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Job Tracker")
        self.master.geometry("600x400")
        
        self.jobs = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        self.job_entry = tk.Entry(self.master, width=40)
        self.job_entry.pack(pady=10)
        
        self.add_button = tk.Button(self.master, text="Add Job", command=self.add_job)
        self.add_button.pack()
        
        self.job_listbox = tk.Listbox(self.master, width=50)
        self.job_listbox.pack(pady=10)
        
        self.stats_button = tk.Button(self.master, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack()
        
    def add_job(self):
        job = self.job_entry.get()
        if job:
            date = datetime.date.today().strftime("%Y-%m-%d")
            if date not in self.jobs:
                self.jobs[date] = []
            self.jobs[date].append(job)
            self.job_listbox.insert(tk.END, f"{date}: {job}")
            self.job_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a job.")
            
    def show_statistics(self):
        if not self.jobs:
            messagebox.showinfo("Info", "No jobs recorded yet.")
            return
        
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Job Statistics")
        stats_window.geometry("800x600")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        dates = list(self.jobs.keys())
        job_counts = [len(jobs) for jobs in self.jobs.values()]
        
        ax1.bar(dates, job_counts)
        ax1.set_title("Jobs per Day")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Number of Jobs")
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        all_jobs = [job for jobs in self.jobs.values() for job in jobs]
        job_freq = {}
        for job in all_jobs:
            job_freq[job] = job_freq.get(job, 0) + 1
        
        top_jobs = sorted(job_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        job_names, job_counts = zip(*top_jobs)
        
        ax2.bar(job_names, job_counts)
        ax2.set_title("Top 5 Most Common Jobs")
        ax2.set_xlabel("Job")
        ax2.set_ylabel("Frequency")
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

root = tk.Tk()
app = JobTracker(root)
root.mainloop()