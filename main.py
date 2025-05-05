import os
import random
from escpos.printer import Usb
from PIL import Image
import keyboard # Import the keyboard library

# --- Configuration ---
# Set the folder where your images are located
IMAGE_FOLDER = 'img' # Create a folder named 'img' in the same directory as your script
# Add your image files (e.g., .png, .jpg) to this folder

# Printer Configuration based on your device details (0x0416:0x5011)
PRINTER_VENDOR_ID = 0x0416
PRINTER_PRODUCT_ID = 0x5011
# These endpoint and interface values are commonly used for this printer model
# Make sure these match the values you found using lsusb or system tools
PRINTER_IN_EP = 0x1
PRINTER_OUT_EP = 0x03
PRINTER_INTERFACE = 0
PRINTER_TIMEOUT = 5000 # Timeout in milliseconds (e.g., 5000 for 5 seconds)
PRINTER_PROFILE = 'POS-5890' # This profile is often compatible with 58mm POS printers

# --- Function to print a random image ---
def print_random_image(printer_obj):
    """Selects a random image from the IMAGE_FOLDER and prints it."""
    print("Spacebar pressed. Attempting to print a random image...")

    # Get a list of all files in the image folder
    try:
        files = os.listdir(IMAGE_FOLDER)
    except FileNotFoundError:
        print(f"Error: Image folder '{IMAGE_FOLDER}' not found.")
        return

    # Filter for common image file extensions
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    if not image_files:
        print(f"No image files found in '{IMAGE_FOLDER}'. Please add some images.")
        return

    # Select a random image filename
    random_image_filename = random.choice(image_files)
    image_path = os.path.join(IMAGE_FOLDER, random_image_filename)

    print(f"Selected image: {random_image_filename}")

    try:
        # Load the image using Pillow (PIL)
        img = Image.open(image_path)
        print(f"Image '{random_image_filename}' loaded successfully.")

        # Print the image
        print("Sending image to printer...")
        # Using 'bitImageColumn' as used before
        printer_obj.image(img, impl='bitImageColumn')
        print("Image sent to printer.")

        # Add some line feeds to push the paper out
        printer_obj.ln(5)
        print("Added line feeds.")

        # Cut the paper (optional, uncomment if your printer supports it)
        # printer_obj.cut()
        # print("Sent cut command (if supported).")

    except Exception as e:
        print(f"An error occurred during printing: {e}")
        # Note: The printer connection remains open to listen for more key presses.
        # Handle specific escpos exceptions if needed for more granular error reporting.


# --- Main Script ---

# Create the image folder if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
    print(f"Created image folder: '{IMAGE_FOLDER}'. Please add images here.")

p = None # Initialize printer object to None

try:
    # Initialize the USB printer with the specified configurations
    p = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID,
            in_ep=PRINTER_IN_EP,
            out_ep=PRINTER_OUT_EP,
            interface=PRINTER_INTERFACE,
            timeout=PRINTER_TIMEOUT,
            profile=PRINTER_PROFILE)

    # Open the printer connection (optional, see previous notes)
    try:
         p.open()
         print("Printer connection attempted (open called).")
    except AttributeError:
         print("p.open() method not available or necessary.")
    except Exception as open_e:
         print(f"Error during printer open: {open_e}")


    print("Printer object created successfully.")
    print("-" * 30)
    print("Press the SPACEBAR key to print a random image.")
    print("Press Ctrl+C to exit the script.")
    print("-" * 30)

    # Set up the hotkey to call the print_random_image function when space is pressed
    # Use lambda to pass the printer object to the function
    keyboard.add_hotkey('space', lambda: print_random_image(p))

    # Keep the script running and listening for key presses
    keyboard.wait()

except Exception as e:
    print(f"\nAn error occurred during printer initialization or keyboard setup: {e}")
    print("Possible issues:")
    print("- Ensure the printer is connected and powered on.")
    print("- Check your PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID, PRINTER_IN_EP, PRINTER_OUT_EP, and PRINTER_INTERFACE values.")
    print("- On Linux, you might need to run this script with 'sudo' or set up a udev rule for your printer.")
    print("- Make sure the 'keyboard' library is installed (`pip install keyboard`).")

finally:
    # Ensure the printer connection is closed when the script exits (e.g., by Ctrl+C)
    if p is not None and hasattr(p, 'close'):
        try:
            p.close()
            print("\nPrinter connection closed.")
        except Exception as close_e:
            print(f"Error closing printer connection: {close_e}")

