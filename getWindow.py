import tkinter as tk
import socket
import base64
from PIL import Image
from io import BytesIO

class EmailViewerApp:
  def __init__(self, master):
    self.master = master
    master.title("Email Viewer")

    # Email List
    self.email_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    self.email_listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.email_listbox.bind('<<ListboxSelect>>', self.show_messages)

    # Message List
    self.message_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    self.message_listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.message_listbox.bind('<<ListboxSelect>>', self.show_email_content)

    # Email Content
    self.email_content_text = tk.Text(master, wrap=tk.WORD, height=10, width=40)
    self.email_content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Initialize data (replace this with actual data retrieval logic)
    self.email_addresses = []
    self.messages = {}
    self.email_content = {
        "Meeting Tomorrow": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Project Update": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Review Proposal": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "Follow-up": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    }
    self.sock()


    # Populate email list
    for email in self.email_addresses:
      self.email_listbox.insert(tk.END, email)

  def show_messages(self, event):
    selected_email_index = self.email_listbox.curselection()
    if selected_email_index:
      selected_email = self.email_listbox.get(selected_email_index)
      messages = self.messages.get(selected_email, [])
      self.message_listbox.delete(0, tk.END)  # Clear previous messages
      for message in messages:
        self.message_listbox.insert(tk.END, message)

  def show_email_content(self, event):
    selected_message_index = self.message_listbox.curselection()
    if selected_message_index:
      selected_message = self.message_listbox.get(selected_message_index)
      email_content = self.email_content.get(selected_message, "")
      self.email_content_text.delete(1.0, tk.END)  # Clear previous content
      self.email_content_text.insert(tk.END, email_content)

  def receive_data(self, sock):
    email_data = b''
    while True:
      part = sock.recv(4096)
      email_data += part
      if len(part) < 4096:
        break

    return email_data
  
  def check(self, base64_string):
    try:
      image_data = base64.b64decode(base64_string)
      image_buffer = BytesIO(image_data)
      return 1
    except:
      return 0
    
  def get_img(self, b):
    if b.startswith('data:image'):
      b = b.split(',')[1]

    print("1")
    # print(b)

    try:
      image_data = base64.b64decode(b)
      image_buffer = BytesIO(image_data)
      image = Image.open(image_buffer)
      return image
    except Exception as e:
      print("none")
      return None
  
  def get_file(self, b):
    if b[:4] == "/9j/":
      image = self.get_img(b)
      if image:
        image.show()
      return

    if b[:3] == "JVB":
      with open('output.pdf', 'wb') as file:
        file.write(base64.b64decode(b))
    
    with open('output.txt', 'wb') as file:
      file.write(base64.b64decode(b))

  def sock(self):
    email_address = "a@gmail.com"
    password = "your_password"

    pop_conn = socket.socket()
    pop_conn.connect(("localhost", 3335))

    recv = pop_conn.recv(1024).decode()
    print(recv)

    pop_conn.send(f'USER {email_address}\r\n'.encode())
    print(pop_conn.recv(1024).decode())

    pop_conn.send(f'PASS {password}\r\n'.encode())
    print(pop_conn.recv(1024).decode())

    pop_conn.sendall(b'STAT\r\n')
    response = pop_conn.recv(1024).decode()
    print(response)

    pop_conn.send(b'LIST\r\n')
    message_list = pop_conn.recv(1024).decode()
    print(message_list)

    pop_conn.send(b'UIDL\r\n')
    response = pop_conn.recv(1024).decode()

    for k in range(1, len(message_list.split()), 2):
      pop_conn.send(f'RETR {message_list.split()[k]}\r\n'.encode())
      email_data = self.receive_data(pop_conn)
      email_text = email_data.decode()
      email_parts = email_text.split()

      print(email_parts)

      b = ""
      content = ""
      flag = 0
      for i, part in enumerate(email_parts):
        if part[:4] == "From":
          content += part
          content += email_parts[i+1]
          i + 1
          content+= '\n'
          if part.split(":")[1].strip() not in self.email_addresses:
            self.email_addresses.append(part.split(":")[1].strip()) 
            self.messages[part.split(":")[1].strip()] = []
          self.messages[part.split(":")[1].strip()].append(response.split()[k + 1])

          continue
          
        if part[:3] == "To:":
          content += part
          content += email_parts[i+1]
          i + 1
          content += '\n'
          continue

        if part == "":
          continue

        if part[:4] == "name" or part[:8] == "filename":
          continue

        if part[:3] == "+OK":
          email_parts[i+1] =""
          continue

        if part[:4] == "Date":
          email_parts[i + 1] = ""
          content += part
          content += email_parts[i + 2]
          content += '\n'
          email_parts[i+2] = ""
          continue

        if part[:7] == "Subject":
          content += part
          content += email_parts[i+1]
          i = i + 1
          content += '\n\n'
          continue

        if part[:12] == "Content-Type":
          flag = 1
          self.email_content[response.split()[k + 1]] = content

        if self.check(part) == 0 and flag == 0:
          content += part
          
        if self.check(part) == 1:
          if flag == 0:
            self.email_content[response.split()[k + 1]] = content
          flag = 1 
          b += part
        if part[:12] == "Content-Type" or part == ".":
          if b != "":
            self.get_file(b)
            b = ""



def main():
  root = tk.Tk()
  app = EmailViewerApp(root)
  root.mainloop()

if __name__ == "__main__":
  main()
