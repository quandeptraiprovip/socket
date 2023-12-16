import tkinter as tk
from tkinter import filedialog
import socket 
import base64
import os
from datetime import datetime
import choice

class SendWindow:
  def __init__(self, master, email):
    self.master = master
    master.title("Email Client")
    self.email = email

    for i in range(9):  # Increased the range to accommodate the new row
      master.columnconfigure(i, weight=1)
      master.rowconfigure(i, weight=1)

    self.to_label = tk.Label(master, text="To:")
    self.to_label.grid(row=0, column=0, sticky="e")

    self.to_email_entry = tk.Entry(master)
    self.to_email_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

    self.cc_lable = tk.Label(master, text="Cc:")
    self.cc_lable.grid(row=1, column=0, sticky="e")

    self.cc_email_entry = tk.Entry(master)
    self.cc_email_entry.grid(row=1, column=1, columnspan=4, sticky="ew")

    self.bcc_label = tk.Label(master, text="Bcc:")
    self.bcc_label.grid(row=2, column=0, sticky="e")

    self.bcc_email_entry = tk.Entry(master)
    self.bcc_email_entry.grid(row=2, column=1, columnspan=4, sticky="ew")

    self.from_label = tk.Label(master, text="From:")
    self.from_label.grid(row=3, column=0, sticky="e")

    self.from_email_entry = tk.Entry(master)
    self.from_email_entry.grid(row=3, column=1, columnspan=4, sticky="ew")
    self.from_email_entry.insert(0, f"{email}")

    self.subject_label = tk.Label(master, text="Subject:")
    self.subject_label.grid(row=4, column=0, sticky="e")

    self.subject_entry = tk.Entry(master)
    self.subject_entry.grid(row=4, column=1, columnspan=4, sticky="ew")

    self.content_label = tk.Label(master, text="Email Content:")
    self.content_label.grid(row=5, column=0, sticky="ne")

    self.email_content_text = tk.Text(master, wrap="word", width=40, height=10)
    self.email_content_text.grid(row=5, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

    self.attach_button = tk.Button(master, text="Attach File", command=self.attach_file)
    self.attach_button.grid(row=6, column=1, columnspan=2, sticky="ew")

    self.attached_files_list = []
    self.attached_files = tk.StringVar()
    self.attached_files_label = tk.Label(master, textvariable=self.attached_files, wraplength=400)
    self.attached_files_label.grid(row=6, column=3, columnspan=2, sticky="ew")

    self.send_button = tk.Button(master, text="Send", command=self.send_email)
    self.send_button.grid(row=7, column=1, columnspan=3, sticky="ew")

    self.back_button = tk.Button(master, text="Back", command=self.go_back)
    self.back_button.grid(row=8, column=1, columnspan=2, sticky="ew")

  def clear_window(self):
    for widget in self.master.winfo_children():
        widget.destroy()

  def go_back(self):
    self.clear_window()
    choice.Choices(self.master, self.email)


  def attach_file(self):
    file_paths = filedialog.askopenfilenames()
    print("Files attached:", file_paths)
    self.attached_files_list.clear()
    self.attached_files_list.extend(file_paths)
    self.attached_files.set(", ".join(self.attached_files_list))

  def send_email(self):
    to_addresses = self.to_email_entry.get().split(',')
    bcc_addresses = self.bcc_email_entry.get().split(',')
    cc_addresses = self.cc_email_entry.get()
    cc_address = cc_addresses.split(',')
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

    if to_addresses:
      for to_address in to_addresses:
        self.sock(to_address)

    if bcc_addresses:
      for bcc_address in bcc_addresses:
        self.sock(bcc_address)
    
    if cc_addresses:
      for address in cc_address:
        self.sock_cc(cc_addresses, address)


  def sock_cc(self, emails, email) :
    s = socket.socket()
    s.connect(("localhost", 2225))

    recv1 = s.recv(1024).decode() 
    print(recv1)


    s.send(f'MAIL FROM: <{self.email}>\r\n'.encode())
    recv1 = s.recv(1024).decode() 
    print(recv1)


    s.send(f'RCPT TO: <{email}>\r\n'.encode())
    recv1 = s.recv(1024).decode()
    print(recv1)

    s.send(b'DATA\r\n')
    recv1 = s.recv(1024).decode() 
    print(recv1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("Date: %Y/%m/%d_%H:%M:%S")

    email_content = self.email_content_text.get("1.0", "end-1c")

    message = f"Date: {formatted_datetime}\r"\
              f"\r\nFrom:{self.email}"\
              f"\r\nTo:{emails}\r\n"\
              f"\r\nSubject: {self.subject_entry.get()}\r\n"\
              f"\r\n{email_content}\r\n"\
              
    s.send(message.encode())

    for file in self.attached_files_list:
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

  def sock(self, email):
    s = socket.socket()
    s.connect(("localhost", 2225))

    recv1 = s.recv(1024).decode() 
    print(recv1)


    s.send(f'MAIL FROM: <{self.email}>\r\n'.encode())
    recv1 = s.recv(1024).decode() 
    print(recv1)


    s.send(f'RCPT TO: <{email}>\r\n'.encode())
    recv1 = s.recv(1024).decode()
    print(recv1)

    s.send(b'DATA\r\n')
    recv1 = s.recv(1024).decode() 
    print(recv1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("Date: %Y/%m/%d_%H:%M:%S")

    email_content = self.email_content_text.get("1.0", "end-1c")

    message = f"Date: {formatted_datetime}\r"\
              f"\r\nFrom:{self.email}"\
              f"\r\nTo:{email}\r\n"\
              f"\r\nSubject: {self.subject_entry.get()}\r\n"\
              f"\r\n{email_content}\r\n"\
              
    s.send(message.encode())

    for file in self.attached_files_list:
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


def main():
  root = tk.Tk()
  app = SendWindow(root, "abc")
  root.mainloop()

if __name__ == "__main__":
  main()
