import tkinter as tk
from tkinter import filedialog
import socket 
import base64
import os
from datetime import datetime

class SendWindow:
  def __init__(self, master, email):
    self.master = master
    master.title("Email Client")

    for i in range(8):  # Increased the range to accommodate the new row
      master.columnconfigure(i, weight=1)
      master.rowconfigure(i, weight=1)

    self.to_label = tk.Label(master, text="To:")
    self.to_label.grid(row=0, column=0, sticky="e")

    self.to_email_entry = tk.Entry(master)
    self.to_email_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

    self.bcc_label = tk.Label(master, text="Bcc:")
    self.bcc_label.grid(row=1, column=0, sticky="e")

    self.bcc_email_entry = tk.Entry(master)
    self.bcc_email_entry.grid(row=1, column=1, columnspan=4, sticky="ew")

    self.from_label = tk.Label(master, text="From:")
    self.from_label.grid(row=2, column=0, sticky="e")

    self.from_email_entry = tk.Entry(master)
    self.from_email_entry.grid(row=2, column=1, columnspan=4, sticky="ew")
    self.from_email_entry.insert(0, f"{email}")

    self.subject_label = tk.Label(master, text="Subject:")
    self.subject_label.grid(row=3, column=0, sticky="e")

    self.subject_entry = tk.Entry(master)
    self.subject_entry.grid(row=3, column=1, columnspan=4, sticky="ew")

    self.content_label = tk.Label(master, text="Email Content:")
    self.content_label.grid(row=4, column=0, sticky="ne")

    self.email_content_text = tk.Text(master, wrap="word", width=40, height=10)
    self.email_content_text.grid(row=4, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

    self.attach_button = tk.Button(master, text="Attach File", command=self.attach_file)
    self.attach_button.grid(row=5, column=1, columnspan=2, sticky="ew")

    self.attached_files_list = []
    self.attached_files = tk.StringVar()
    self.attached_files_label = tk.Label(master, textvariable=self.attached_files, wraplength=400)
    self.attached_files_label.grid(row=5, column=3, columnspan=2, sticky="ew")

    self.send_button = tk.Button(master, text="Send", command=self.send_email)
    self.send_button.grid(row=6, column=1, columnspan=3, sticky="ew")

  def attach_file(self):
    file_paths = filedialog.askopenfilenames()
    print("Files attached:", file_paths)
    self.attached_files_list.clear()
    self.attached_files_list.extend(file_paths)
    self.attached_files.set(", ".join(self.attached_files_list))

  def send_email(self):
    to_addresses = self.to_email_entry.get().split(',')
    bcc_addresses = self.bcc_email_entry.get().split(',')
    from_email = self.from_email_entry.get()
    subject = self.subject_entry.get()
    email_content = self.email_content_text.get("1.0", "end-1c")
    files = self.attached_files_list

    print("To: ", to_addresses)
    print("Bcc: ", bcc_addresses)
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

    if bcc_addresses:
      for bcc_email in bcc_addresses:
          s.send(f'RCPT TO: <{bcc_email}>\r\n'.encode())
          recv1 = s.recv(1024).decode()
          print(recv1)

    s.send(b'DATA\r\n')
    recv1 = s.recv(1024).decode() 
    print(recv1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("Date: %Y/%m/%d_%H:%M:%S")



    message = f"Date: {formatted_datetime}\r"\
              f"\r\nFrom:{from_email}"\
              f"\r\nTo:{', '.join(to_addresses)}\r\n"\
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

    self.attached_files_list.clear()


def main():
  root = tk.Tk()
  app = SendWindow(root, "abc")
  root.mainloop()

if __name__ == "__main__":
  main()
