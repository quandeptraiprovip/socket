import socket
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime

def check(base64_string):
  try:
    image_data = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_data)
    return 1
  except:
    return 0

def get_attach(base64_string):
  if base64_string.startswith('data:image'):
    base64_string = base64_string.split(',')[1]
  
  print(base64_string )

  try:
    image_data = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_data)
    # image = Image.open(image_buffer)

    print("yes")
    return image
  except:
    print("none")
    return None

  # Open the image using Pillow
  # image = Image.open(image_buffer)

  # return image

email_address = "ttmq38@gmail.com"
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
# print(message_list.split())

pop_conn.send(b'UIDL\r\n')
response = pop_conn.recv(1024).decode()


# for i in range(1, len(message_list.split()), 2):

# pop_conn.send(f'RETR {message_list.split()[i]}\r\n'.encode())
pop_conn.send(f'RETR 27\r\n'.encode())
email_data = b''
while True:
  part = pop_conn.recv(4096)
  email_data += part
  if len(part) < 4096:
    break

email_text = email_data.decode()

email_parts = email_text.split()

b = ""
for part in email_parts:
  if part[:13] == "attached-file":
    b = ""
  else:
    if part[:12] == "Content-Type" or part == ".":
      continue
    else:
      b += part

print(b)

if b.startswith('data:image'):
  b = b.split(',')[1]

    # Decode the base64 string
image_data = base64.b64decode(b)

# Create a BytesIO object to read the image data
image_buffer = BytesIO(image_data)

# Open the image using Pillow
image = Image.open(image_buffer)

# Save the image with the new filename
# image.save(filename)

image.show()



pop_conn.send(b'QUIT\r\n')
print(pop_conn.recv(1024).decode())
pop_conn.close()
