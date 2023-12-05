import tkinter as tk
from tkinter import filedialog
import socket 
import base64
import os
from datetime import datetime

def attach_file():
  file_paths = filedialog.askopenfilenames()
  print("Files attached:", file_paths)
  attached_files_list.clear()
  attached_files_list.extend(file_paths)
  attached_files.set(", ".join(attached_files_list))

def send_email():
  to_email = to_email_entry.get()
  from_email = from_email_entry.get()
  subject = subject_entry.get()
  email_content = email_content_text.get("1.0", "end-1c")
  files = attached_files_list

  print("To: ", to_email)
  print("From: ", from_email)
  print("Subject: ", subject)
  print("Email Content:", email_content)
  print("Attached Files:", files)

  s = socket.socket()
  s.connect(("localhost", 2225))

  recv1 = s.recv(1024).decode() 
  print(recv1)


  s.send(f'MAIL FROM: <{from_email}>\r\n'.encode())
  recv1 = s.recv(1024).decode() 
  print(recv1)


  s.send(f'RCPT TO: <{to_email}>\r\n'.encode())
  recv1 = s.recv(1024).decode() 
  print(recv1)

  s.send(b'DATA\r\n')
  recv1 = s.recv(1024).decode() 
  print(recv1)

  current_datetime = datetime.now()
  formatted_datetime = current_datetime.strftime("Date: %Y/%m/%d_%H:%M:%S")



  message = f"Date: {formatted_datetime}\r"\
            f"\r\nFrom:{from_email}"\
            f"\r\nTo:{to_email}\r\n"\
            f"\r\nSubject: {subject}\r\n"\
            f"\r\n{email_content}\r\n"\
            
  s.send(message.encode())

  for file in files:
    with open(file, "rb") as attachment:
      print(file)
      file_name = os.path.basename(file)
      attachment_content = f"\r\nContent-Type: application/octet-stream; name={file_name}\r\n" \
                          f"Content-Transfer-Encoding: base64\r\n" \
                          f"Content-Disposition: attachment; filename={file_name}\r\n\r\n" \
                          # f"attached-file\r\n\r\n"
      s.send(attachment_content.encode())

      while True:
        chunk = attachment.read(1023)
        if not chunk:
            break
        encoded_chunk = base64.b64encode(chunk).decode()
        s.send(f'{encoded_chunk}\r\n'.encode())


  s.send(".\r\n".encode())
  s.send("QUIT\r\n".encode())
  s.close()

  attached_files_list.clear()

window = tk.Tk()
window.title("Email Client")

for i in range(6):  # Increased the range to accommodate the new row
  window.columnconfigure(i, weight=1)
  window.rowconfigure(i, weight=1)

to_label = tk.Label(window, text="To:")
to_label.grid(row=0, column=0, sticky="e")

to_email_entry = tk.Entry(window)
to_email_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

from_label = tk.Label(window, text="From:")
from_label.grid(row=1, column=0, sticky="e")

from_email_entry = tk.Entry(window)
from_email_entry.grid(row=1, column=1, columnspan=4, sticky="ew")
from_email_entry.insert(0, "a@gmail.com")

subject_label = tk.Label(window, text="Subject:")
subject_label.grid(row=2, column=0, sticky="e")

subject_entry = tk.Entry(window)
subject_entry.grid(row=2, column=1, columnspan=4, sticky="ew")

content_label = tk.Label(window, text="Email Content:")
content_label.grid(row=3, column=0, sticky="ne")

email_content_text = tk.Text(window, wrap="word", width=40, height=10)
email_content_text.grid(row=3, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

attach_button = tk.Button(window, text="Attach File", command=attach_file)
attach_button.grid(row=4, column=1, columnspan=2, sticky="ew")

attached_files_list = []
attached_files = tk.StringVar()
attached_files_label = tk.Label(window, textvariable=attached_files, wraplength=400)
attached_files_label.grid(row=4, column=3, columnspan=2, sticky="ew")

send_button = tk.Button(window, text="Send", command=send_email)
send_button.grid(row=5, column=1, columnspan=3, sticky="ew")

window.mainloop()
