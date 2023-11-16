import socket

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
print(message_list.split())

pop_conn.send(b'UIDL\r\n')
response = pop_conn.recv(1024).decode()
print(response)


for i in range(1, len(message_list.split()), 2):
    if message_list.split()[i] == '.': break

    pop_conn.send(f'RETR {message_list.split()[i]}\r\n'.encode())
    email_data = b''
    while True:
        part = pop_conn.recv(4096)
        email_data += part
        if len(part) < 4096:
            break
    
email_text = email_data.decode()
print(email_text)

aa = email_text.split()
print(aa)

pop_conn.send(b'QUIT\r\n')
print(pop_conn.recv(1024).decode())
pop_conn.close()
