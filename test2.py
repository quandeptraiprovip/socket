import tkinter as tk

def open_compose_frame(sender_name):
    sender_frame.pack_forget()  # Hide the sender frame
    compose_frame.pack()  # Show the compose frame

    # Update label in the compose frame with sender's name
    compose_label.config(text=f"Compose Email for {sender_name}")

def get_sender_name():
    sender_name = sender_entry.get()
    if sender_name:
        open_compose_frame(sender_name)
    else:
        feedback_label.config(text="Please enter the sender's name")

# Create the main window
root = tk.Tk()
root.title("Email Application")

# Create frames for sender and compose sections
sender_frame = tk.Frame(root)
compose_frame = tk.Frame(root)

# Add widgets for entering sender information
sender_label = tk.Label(sender_frame, text="Enter Sender's Name:")
sender_label.pack()

sender_entry = tk.Entry(sender_frame)
sender_entry.pack()

feedback_label = tk.Label(sender_frame, text="")
feedback_label.pack()

submit_button = tk.Button(sender_frame, text="Submit", command=get_sender_name)
submit_button.pack()

# Add widgets for composing email in the compose frame
compose_label = tk.Label(compose_frame, text="")
compose_label.pack()

# Add more widgets for email composition as needed

# Initially, show the sender frame and hide the compose frame
sender_frame.pack()
compose_frame.pack_forget()

root.mainloop()
