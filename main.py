import os
from escpos.printer import Usb
from PIL import Image

# --- Configuration ---
# Replace with the filename of the image in the same folder
IMAGE_FILENAME = 'your_image.png'

# Printer Configuration from the original code
PRINTER_VENDOR_ID = "0x0416"
PRINTER_PRODUCT_ID = "0x5011"
PRINTER_IN_EP = "0x1"
PRINTER_OUT_EP = "0x03"
PRINTER_INTERFACE = "0"
PRINTER_TIMEOUT = "0"
PRINTER_PROFILE = 'POS-5890'

# --- Main Script ---

# Construct the full path to the image file
# This assumes the image is in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, IMAGE_FILENAME)


# Check if the image file exists
if not os.path.exists(image_path):
    print(f"Error: Image file '{IMAGE_FILENAME}' not found at '{image_path}'. Make sure it's in the same folder.")
else:
    try:
        # Initialize the USB printer with the specified configurations
        p = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID,
                in_ep=PRINTER_IN_EP,
                out_ep=PRINTER_OUT_EP,
                interface=PRINTER_INTERFACE,
                timeout=PRINTER_TIMEOUT,
                profile=PRINTER_PROFILE)

        # Open the printer connection
        p.open()
        print("Printer connected.")

        # Clear the printer buffer (ESC @ command - optional, keep if it was useful)
        # p._raw(b'\x1b\x40')

        # Load the image using Pillow (PIL)
        img = Image.open(image_path)
        print(f"Image '{IMAGE_FILENAME}' loaded successfully.")

        # Print the image
        # Using 'bitImageColumn' as in the original code's printImages function
        p.image(img, impl='bitImageColumn')
        print("Image sent to printer.")

        # Add some line feeds to push the paper out
        p.ln(5)

        # Cut the paper (optional, uncomment if your printer supports it)
        # p.cut()

        # Close the printer connection
        p.close()
        print("Printer connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Attempt to close the printer connection if it was opened
        if 'p' in locals() and hasattr(p, 'close'):
             try:
                 p.close()
                 print("Printer connection closed due to error.")
             except Exception as close_e:
                 print(f"Error closing printer connection after error: {close_e}")