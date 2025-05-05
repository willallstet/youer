import os
from escpos.printer import Usb
from PIL import Image

# --- Configuration ---
# Replace with the filename of the image in the same folder
IMAGE_FILENAME = 'your_image.png' # Make sure you have an image file named 'your_image.png' in the same directory as your script.

# Printer Configuration based on your device details (0x0416:0x5011)
PRINTER_VENDOR_ID = 0x0416
PRINTER_PRODUCT_ID = 0x5011
# These endpoint and interface values are commonly used for this printer model
PRINTER_IN_EP = 0x1
PRINTER_OUT_EP = 0x03
PRINTER_INTERFACE = 0
PRINTER_TIMEOUT = 0 # Timeout in milliseconds (0 means no timeout)
PRINTER_PROFILE = 'POS-5890' # This profile is often compatible with 58mm POS printers

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
        # The commented-out line below was the original incorrect one
        # p = Usb(0x2730, 0x0fff, 0, 0x81, 0x02)

        p = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID,
                in_ep=PRINTER_IN_EP,
                out_ep=PRINTER_OUT_EP,
                interface=PRINTER_INTERFACE,
                timeout=PRINTER_TIMEOUT,
                profile=PRINTER_PROFILE)


        # Open the printer connection (This might happen implicitly on some systems/versions,
        # but explicitly calling it is good practice if available and needed)
        # Check python-escpos documentation for the exact method if 'open()' causes an error.
        # Some versions might handle connection on instantiation or the first print command.
        # Try running without p.open() first if it gives an error.
        try:
             p.open()
             print("Printer connection attempted (open called).")
        except AttributeError:
             print("p.open() method not available or necessary.")
        except Exception as open_e:
             print(f"Error during printer open: {open_e}")


        print("Printer object created.")

        # Clear the printer buffer (ESC @ command - optional, keep if it was useful)
        # p._raw(b'\x1b\x40') # Use with caution, might not be necessary or correct for all printers

        # Load the image using Pillow (PIL)
        img = Image.open(image_path)
        print(f"Image '{IMAGE_FILENAME}' loaded successfully.")

        # Print the image
        # Using 'bitImageColumn' as in the original code's printImages function
        print("Sending image to printer...")
        p.image(img, impl='bitImageColumn')
        print("Image sent to printer.")

        # Add some line feeds to push the paper out
        p.ln(5)
        print("Added line feeds.")

        # Cut the paper (optional, uncomment if your printer supports it)
        # p.cut()
        # print("Sent cut command (if supported).")

        # Close the printer connection
        # Similar to open(), closing might be automatic or not explicitly needed depending on the version.
        # Try running without p.close() first if it gives an error.
        try:
            p.close()
            print("Printer connection closed.")
        except AttributeError:
            print("p.close() method not available or necessary.")
        except Exception as close_e:
            print(f"Error during printer close: {close_e}")


    except Exception as e:
        print(f"An error occurred: {e}")
        # Attempt to close the printer connection if it was opened and the close method exists
        if 'p' in locals() and hasattr(p, 'close'):
             try:
                 p.close()
                 print("Printer connection closed due to error.")
             except Exception as close_e_after_error:
                 print(f"Error closing printer connection after error: {close_e_after_error}")
