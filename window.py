import tkinter as tk
from tkinter import filedialog

def attach_file():
    file_paths = filedialog.askopenfilenames()
    # You can handle the file_paths as needed, for now, let's just print them
    print("Files attached:", file_paths)
    attached_files.set(file_paths)

def send_email():
    to_email = to_email_entry.get()
    from_email = from_email_entry.get()
    email_content = email_content_text.get("1.0", "end-1c")
    files = attached_files.get()

    # You can add the logic to send the email with the specified details
    print("To:", to_email)
    print("From:", from_email)
    print("Email Content:", email_content)
    print("Attached Files:", files)
    # Add logic to send email here

# Create the main window
window = tk.Tk()
window.title("Email Client")

# Configure columns and rows to expand with the window
for i in range(5):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)

# To Email
to_label = tk.Label(window, text="To:")
to_label.grid(row=0, column=0, sticky="e")

to_email_entry = tk.Entry(window)
to_email_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

# From Email
from_label = tk.Label(window, text="From:")
from_label.grid(row=1, column=0, sticky="e")

from_email_entry = tk.Entry(window)
from_email_entry.grid(row=1, column=1, columnspan=4, sticky="ew")

# Email Content
content_label = tk.Label(window, text="Email Content:")
content_label.grid(row=2, column=0, sticky="ne")

email_content_text = tk.Text(window, wrap="word", width=40, height=10)
email_content_text.grid(row=2, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

# Attach File Button
attach_button = tk.Button(window, text="Attach File", command=attach_file)
attach_button.grid(row=3, column=1, columnspan=2, sticky="ew")

# Attached Files Label
attached_files = tk.StringVar()
attached_files_label = tk.Label(window, textvariable=attached_files, wraplength=400)
attached_files_label.grid(row=3, column=3, columnspan=2, sticky="ew")

# Send Button
send_button = tk.Button(window, text="Send", command=send_email)
send_button.grid(row=4, column=1, columnspan=3, sticky="ew")

# Run the Tkinter event loop
window.mainloop()
