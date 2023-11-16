import base64
from PIL import Image
from io import BytesIO

files = ["IMG_9946.JPG"]

for file in files:
  with open(file, "rb") as attachment:
    base64_string = base64.b64encode(attachment.read()).decode()
    # print(content)

    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Create a BytesIO object to read the image data
    image_buffer = BytesIO(image_data)

    # Open the image using Pillow
    image = Image.open(image_buffer)

    image.show()

