import qrcode
import os

# Data to be encoded

# Define the output directory
output_dir = "../IMG"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

import json

# Step 1: Read the JSON file
with open('qr.json', 'r') as file:
    data = json.load(file)

# Step 2: Loop through the data
    
for item in data:
# Create a QR Code object
    url = "https://maps.app.goo.gl/"+item

    # Extract the last part of the URL to use as the filename
    filename = url.split("/")[-1] + ".png"

    qr = qrcode.QRCode(
        version=1,  # Version defines the size of the QR Code (1 is the smallest).
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code grid
        border=1,  # Thickness of the border (minimum is 4)
    )

    # Add data to the QR Code object
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image of the QR Code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image with the dynamic filename
    output_path = os.path.join(output_dir, filename)
    img.save(output_path)

    print(f"QR code generated and saved as '{output_path}'")
