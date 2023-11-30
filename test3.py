str = """
Date: Date: 2023/11/26_08:47:28

From:ttmq38@gmail.com
To:a@gmail.com

Subject: 123

123

Content-Type: application/octet-stream; name=IMG_9946.JPG
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=IMG_9946.JPG

Content-Type: application/octet-stream; name=IMG_9946.JPG
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=IMG_9946.JPG

"""

print(str.partition("Content-Type:"))

