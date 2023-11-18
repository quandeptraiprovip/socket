import socket
import base64

files = ["IMG_9946.JPG"]

s = socket.socket()
s.connect(("localhost", 2225)) 
s.send(b'EHLO example.com\r\n')

sender_email = "ttmq38@gmail.com"
s.send(f'MAIL FROM: <{sender_email}>\r\n'.encode())

receiver_email = "ttmq38@gmail.com"
s.send(f'RCPT TO: <{receiver_email}>\r\n'.encode())

s.send(b'DATA\r\n')

for file in files:
  with open(file, 'rb') as f:
    # image_data = f.read(1023)
    # encoded_chunk = base64.b64encode(image_data).decode()
    # print(encoded_chunk)

    # while image_data:
    #   s.send(f'{encoded_chunk}\r\n'.encode())
    #   image_data = f.read(1023)
    #   encoded_chunk = base64.b64encode(image_data).decode()
    while True:
      chunk = f.read(1024)
      if not chunk:
          break
      encoded_chunk = base64.b64encode(chunk).decode()
      # encoded_chunk = base64.b64encode(chunk)
      s.send(f'{encoded_chunk}\r\n'.encode())



s.send(".\r\n".encode())
s.send("QUIT\r\n".encode())
s.close()