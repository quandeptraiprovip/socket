import tkinter as tk
from tkinter import *
import socket
import base64
from PIL import Image, ImageTk
from io import BytesIO
from configparser import ConfigParser
import choice2

class EmailViewerApp:
  def __init__(self, master, email):
    self.master = master
    master.title("Email Viewer")
    master.geometry("1000x300")

    self.email = email

    # Email List
    self.email_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    self.email_listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.email_listbox.bind('<<ListboxSelect>>', self.show_email_content)

    # Message List
    # self.message_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    # self.message_listbox.pack(side=tk.LEFT, fill=tk.Y)
    # self.message_listbox.bind('<<ListboxSelect>>', self.show_email_content)

    # Email Content
    self.email_content_text = tk.Text(master, wrap=tk.WORD, height=10, width=40)
    self.email_content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    back_button = tk.Button(master, text="Back", command=self.go_back)
    back_button.pack(side=tk.TOP, padx=10, pady=10)

    # Initialize data (replace this with actual data retrieval logic)
    self.tk_image = None
    self.email_addresses = []
    self.messages = {}
    self.email_content = {}
    self.email_status = {}
    self.email_client = {}
    self.email_client[self.email] = {}
    self.ahihu = []
    
    self.read_file()
    self.sock()
    # print(self.messages)
    # print(self.ahihu)

    # config = ConfigParser()
    # config.read("config.ini")
    # config_data = config["AutoUpdate"]

    all_messages = list(self.messages.keys())
    for str in all_messages:
      self.email_listbox.insert(tk.END, str)



    
    # self.auto_check_interval = config_data["time"]

    # self.master.after(0, self.auto_check_and_update)

  def clear_window(self):
    for widget in self.master.winfo_children():
        widget.destroy()

  def go_back(self):
    self.clear_window()
    choice2.Choice(self.master, self.email)

  def read_file(self):
    file = open("ahihu.txt", "r")
    parts = file.read()

    all_parts = parts.split("---")

    email = ""
    for i in range(0, all_parts.len()):
        self.ahihu.append(all_parts[i])
      
  def auto_check_and_update(self):
    # Perform the email check here
    self.sock()
    # print(self.email_addresses)

    # Clear and repopulate the email_listbox with updated data
    self.email_listbox.delete(0, tk.END)
    for email in self.email_addresses:
        self.email_listbox.insert(tk.END, email)

    # Schedule the next auto-check and update
    self.master.after(self.auto_check_interval, self.auto_check_and_update)



  def check(self, base64_string):
    try:
      image_data = base64.b64decode(base64_string)
      image_buffer = BytesIO(image_data)
      return 1
    except:
      return 0
    
  def get_file(self, b):
    if b[:4] == "/9j/":
      image = self.get_img(b)
      # if image:
        # image.show()
      return image

    if b[:3] == "JVB":
      with open('output.pdf', 'wb') as file:
        file.write(base64.b64decode(b))
    
    with open('output.txt', 'wb') as file:
      file.write(base64.b64decode(b))
  
  def get_img(self, b):
    if b.startswith('data:image'):
      b = b.split(',')[1]

    # print("1")
    # print(b)

    try:
      image_data = base64.b64decode(b)
      image_buffer = BytesIO(image_data)
      image = Image.open(image_buffer)
      return image
    except Exception as e:
      print("none")
      return None

  def update_email_list(self, message_index, message):
    self.message_listbox.delete(message_index, message_index)
    self.message_listbox.insert(message_index, message.split('●')[0])

  def show_messages(self, event):
    ...


  def show_email_content(self, event):
    selected_message_index = self.email_listbox.curselection()
    if selected_message_index:
      selected_message = self.email_listbox.get(selected_message_index)
      email_content = self.messages[selected_message]

      parts = email_content.partition("Content-Type:")

      self.email_content_text.delete(1.0, tk.END) # Clear previous content
      self.email_content_text.insert(tk.END, parts[0][8:])

      b = ""
      img_text = parts[2].split()
      for part in img_text:
        if part[:4] == "name" or part[:8] == "filename": 
          continue
        if self.check(part) == 1: 
          b += part
        if part[:12] == "Content-Type" or part == ".":
          if b != "":
            image = self.get_file(b)
            if image:
              # resized_image = image.resize((100, 100), Image.ANTIALIAS)
              self.tk_image = ImageTk.PhotoImage(image)
              label = tk.Label(self.email_content_text, image=self.tk_image)
              label.image = self.tk_image
              self.email_content_text.window_create(tk.END, window=label)

            # if b.startswith('JVBERi'):
            #   # Display PDF
            #   pdf_data = base64.b64decode(b)
            #   pdf_buffer = BytesIO(pdf_data)
            #   pdf_document = fitz.open(pdf_buffer)
            #   pdf_page = pdf_document.load_page(0)
            #   image = pdf_page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
            #   resized_image = image.resize((100, 100), Image.ANTIALIAS)
            #   self.tk_image = ImageTk.PhotoImage(resized_image)
            #   label = tk.Label(self.email_content_text, image=self.tk_image)
            #   label.image = self.tk_image
            #   self.email_content_text.window_create(tk.END, window=label)
            # print(b)
            b = ""

      # self.email_status[selected_message.split('●')[0]] = "Read"
      # self.email_client[self.email][selected_message.split('●')[0]] = "Read"
      # self.update_email_list(selected_message_index, selected_message)

    

  def receive_data(self, sock):
    email_data = b''
    while True:
      part = sock.recv(4096)
      email_data += part
      if len(part) < 4096:
        break

    return email_data
  

  def read_file(self):
    file = open("ahihu.txt", "r")
    parts = file.read()

    if parts == "":
      return

    all_parts = parts.split("---")

    for i in range(0, len(all_parts)):
      self.ahihu.append(all_parts[i])

    file.close()

  def sock(self):
    for content in self.ahihu:
      for str in content.split():
        name = ""
        if str == '' or str == '\n':
          ...
        if str[:2] == "To":
          
          name = str[3:]

          self.messages[name] = content

  

def main():
  root = tk.Tk()
  app = EmailViewerApp(root, "abc")
  root.mainloop()

if __name__ == "__main__":
  main()
