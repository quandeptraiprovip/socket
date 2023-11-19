
import socket 
import base64
import os

files = ["/Users/minh10hd/Downloads/unnamed.jpg", "/Users/minh10hd/Downloads/22127349-P.jpg"]

s = socket.socket()
s.connect(("localhost", 2225)) 

recv1 = s.recv(1024).decode() 
print(recv1)

sender_email = "abc@gmail.com"
s.send(f'MAIL FROM: <{sender_email}>\r\n'.encode())
recv1 = s.recv(1024).decode() 
print(recv1)

receiver_email = "abc@gmail.com"

s.send(f'RCPT TO: <{receiver_email}>\r\n'.encode())
recv1 = s.recv(1024).decode() 
print(recv1)

s.send(b'DATA\r\n')
recv1 = s.recv(1024).decode() 
print(recv1)

subject = "concac"
body = "day la con cac."
message = f'Subject: {subject}\r\n\r\n{body}\r\n'

s.send(message.encode())

for file in files:
  with open(file, "rb") as attachment:
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
      # encoded_chunk = base64.b64encode(chunk)
      s.send(f'{encoded_chunk}\r\n'.encode())


s.send(".\r\n".encode())


# recv1 = s.recv(1024).decode() 
# print(recv1)

s.send("QUIT\r\n".encode())

s.close()