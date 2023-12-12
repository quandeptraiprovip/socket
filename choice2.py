import tkinter as tk
import spam
import getWindow
import project
import work
import important

class Choice:
  def __init__(self, master, email):
    self.master = master
    master.title("Email App")
    self.email = email
    # Buttons
    inbox_button = tk.Button(master, text="Inbox", command=self.inbox_clicked)
    inbox_button.pack(pady=10)

    work_button = tk.Button(master, text="Work", command=self.work_clicked)
    work_button.pack(pady=10)

    important_button = tk.Button(master, text="Important", command=self.important_clicked)
    important_button.pack(pady=10)

    spam_button = tk.Button(master, text="Spam", command=self.spam_clicked)
    spam_button.pack(pady=10)

    subject_button = tk.Button(master, text="Subject", command=self.subject_clicked)
    subject_button.pack(pady=10)

  def clear_window(self):
    for widget in self.master.winfo_children():
        widget.destroy()

  def inbox_clicked(self):
    self.clear_window()
    getWindow.EmailViewerApp(self.master, self.email)

  def work_clicked(self):
    self.clear_window()
    work.Project(self.master, self.email)

  def important_clicked(self):
    self.clear_window()
    important.Project(self.master, self.email)

  def spam_clicked(self):
    self.clear_window()
    spam.Project(self.master, self.email)

  def subject_clicked(self):
    self.clear_window()
    project.Project(self.master, self.email)
