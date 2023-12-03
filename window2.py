import tkinter as tk

def button_click(button):
    print(f'Button clicked: {button.cget("text")}')
    button.config(fg=bg_color)

# Create the main window
window = tk.Tk()
window.title("Button Window")

# Set the background color
bg_color = window.cget('bg')

# Label to display the message
label_message = tk.Label(window, text="Day la danh sach cac folder trong mailbox cua ban")
label_message.pack(pady=10)

# Create buttons with the same color as the background
button_texts = ["Inbox", "Project", "Important", "Work", "Spam"]
for text in button_texts:
    button = tk.Button(window, text=text, command=lambda b=button, t=text: button_click(b), fg="black")
    button.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()
