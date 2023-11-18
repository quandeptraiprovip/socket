import base64
from PIL import Image
from io import BytesIO
from datetime import datetime

files = ["IMG_9946.JPG"]

for file in files:
  with open(file, "rb") as attachment:
    base64_string = base64.b64encode(attachment.read()).decode()
    print(base64_string)

    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Create a BytesIO object to read the image data
    image_buffer = BytesIO(image_data)

    # Open the image using Pillow
    image = Image.open(image_buffer)
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Add the date and time to the image filename
    filename = f"image_{formatted_datetime}.jpg"

    # Save the image with the new filename
    # image.save(filename)

    image.show()

