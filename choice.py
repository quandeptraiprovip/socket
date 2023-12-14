import tkinter as tk
from tkinter import messagebox
import socket 
import base64
import os
from datetime import datetime
import sendWindow
import getWindow
import choice2
import startwindow

class Choices:

  def __init__(self, master, email):
    self.master = master
    master.title("Email App")
    master.geometry("400x300")

    self.email = email

    # self.back_button = tk.Button(master, text="⬅", font=("Arial", 14, "bold"))
    # self.back_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

    self.send_button = tk.Button(master, text="Send Email", command = self.send)
    self.send_button.pack(pady=10)

    self.read_button = tk.Button(master, text="Read Email", command = self.read)
    self.read_button.pack(pady=10)

    back_button = tk.Button(master, text="Back", command=self.go_back)
    back_button.pack(side=tk.TOP, padx=10, pady=10)

  def send(self):
    self.clear_window()
    sendWindow.SendWindow(self.master, self.email)

  def clear_window(self):
    # Destroy all widgets in the window
    for widget in self.master.winfo_children():
        widget.destroy()
  
  def read(self):
    self.clear_window()
    choice2.Choice(self.master, self.email)

  def go_back(self):
    self.clear_window()
    startwindow.StartWindow(self.master)
