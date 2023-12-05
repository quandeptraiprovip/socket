import tkinter as tk
from tkinter import messagebox
import choice

class StartWindow:
  def __init__(self, master):
    self.master = master
    master.title("Login Window")

    # Create and place the Username label and input box
    self.label_username = tk.Label(master, text="Username:")
    self.label_username.grid(row=0, column=0, padx=10, pady=10)

    self.entry_username = tk.Entry(master)
    self.entry_username.grid(row=0, column=1, padx=10, pady=10)

    # Create and place the Password label and input box
    self.label_password = tk.Label(master, text="Password:")
    self.label_password.grid(row=1, column=0, padx=10, pady=10)

    self.entry_password = tk.Entry(master, show="*")  # Use show="*" to hide the entered characters
    self.entry_password.grid(row=1, column=1, padx=10, pady=10)

    # Create and place the Login button
    self.login_button = tk.Button(master, text="Log In", command=self.on_login_button_click)
    self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

  def on_login_button_click(self):

    username = self.entry_username.get()
    password = self.entry_password.get()

    # Add your login logic here
    # For demonstration purposes, let's just display the entered username and password
    print("Login Info", f"Username: {username}\nPassword: {password}")
    self.clear_window()
    choice.Choices(self.master, username)
    

  def clear_window(self):
    # Destroy all widgets in the window
    for widget in self.master.winfo_children():
        widget.destroy()


  