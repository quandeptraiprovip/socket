
import socket 
from datetime import datetime

s = socket.socket()
s.connect(("localhost", 2225)) 

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("Date: %Y/%m/%d_%H:%M:%S")

recv1 = s.recv(1024).decode() 
print(recv1)

sender_email = "ttmq38@gmail.com"
s.send(f'MAIL FROM: <{sender_email}>\r\n'.encode())
recv1 = s.recv(1024).decode() 
print(recv1)

receiver_email = "ttmq38@gmail.com"

s.send(f'RCPT TO: <{receiver_email}>\r\n'.encode())
recv1 = s.recv(1024).decode() 
print(recv1)

s.send(b'DATA\r\n')
recv1 = s.recv(1024).decode() 
print(recv1)

subject = "concac"
body = "day la con cac."

message = f'{formatted_datetime}\r\nTo: {receiver_email}\r\nFrom: {sender_email}\r\n\r\nSubject: {subject}\r\n\r\n{body}\r\n.\r\n'

s.send(message.encode())
recv1 = s.recv(1024).decode() 
print(recv1)

s.close()