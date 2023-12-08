import socket
import base64

def send_command(socket, command):
    socket.send(command.encode())
    response = socket.recv(1024).decode()
    return response

def login(socket, email_user, email_pass):
    send_command(socket, f"LOGIN {email_user} {email_pass}\r\n")

def select_mailbox(socket, mailbox="inbox"):
    send_command(socket, f"SELECT {mailbox}\r\n")

def search_emails(socket, criteria="ALL"):
    return send_command(socket, f"SEARCH {criteria}\r\n")

def fetch_email(socket, email_number):
    return send_command(socket, f"FETCH {email_number} RFC822\r\n")

def close_connection(socket):
    send_command(socket, "LOGOUT\r\n")
    socket.close()

def filter_email(email_data, sender_filter, content_filter, subject_filter):
    # Xử lý nội dung email và kiểm tra các tiêu chí lọc
    lines = email_data.split('\r\n')
    sender = None
    content = ""
    subject = None
    for line in lines:
        if line.startswith("From:"):
            sender = line[len("From:"):].strip()
        elif line.startswith("Subject:"):
            subject = line[len("Subject:"):].strip()
        content += line + '\r\n'

    # Lọc theo người gửi, subject và nội dung
    if sender_filter and sender_filter.lower() not in sender.lower():
        return None
    if subject_filter and subject_filter.lower() not in subject.lower():
        return None
    if content_filter and content_filter.lower() not in content.lower():
        return None

    return email_data

def search_emails(socket, criteria="ALL"):
    response = send_command(socket, f"SEARCH {criteria}\r\n")
    response_lines = response.split('\r\n')

    # Check for errors
    if "BAD" in response_lines[0] or "NO" in response_lines[0]:
        return response_lines[0], ""

    # Check for empty response
    if len(response_lines) < 3 or not response_lines[2].strip():
        return "NO", ""

    # Extract status and messages
    status = response_lines[0].strip()
    messages = response_lines[2].strip()

    return status, messages


def get_and_filter_emails(email_user, email_pass, sender_filter, content_filter, subject_filter):
    # Kết nối đến máy chủ IMAP
    imap_server = "imap.gmail.com"
    imap_port = 995
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((imap_server, imap_port))
    recv_data = s.recv(1024).decode()
    print(recv_data)

    try:
        # Đăng nhập
        login(s, email_user, email_pass)

        # Chọn thư mục inbox
        select_mailbox(s)

        # Tìm kiếm tất cả email
        status, messages = search_emails(s)
        if status == "OK":
            for email_number in messages.split():
                # Lấy email theo số thứ tự
                status, response = fetch_email(s, email_number)
                if status == "OK":
                    # Lọc email theo các tiêu chí
                    filtered_email = filter_email(response, sender_filter, content_filter, subject_filter)
                    if filtered_email:
                        print(filtered_email)  # In response để xem thông tin email

    finally:
        # Đóng kết nối
        close_connection(s)


# Thông tin tài khoản email
email_user = "your_email@gmail.com"
email_pass = "your_password"

# Tiêu chí lọc
# Tiêu chí lọc
sender_filter = "anhquanbcl@gmail.com"
subject_filter = "Test"
content_filter = "this"



# Gọi hàm để lấy và lọc email
get_and_filter_emails(email_user, email_pass, subject_filter, sender_filter, content_filter)
