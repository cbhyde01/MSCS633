"""
qr_generator.py
---------------
QR Code Generator Application — Biox Systems
Author  : Corey
Course  : MSCS 633 — Assignment 2
Date    : March 15, 2026
Institution: University of the Cumberlands

Description:
    This application prompts the user to enter a URL and generates a
    corresponding QR code image saved to disk.  A QR (Quick Response)
    code is a two-dimensional barcode invented in 1994 by the Japanese
    company Denso Wave.  It encodes data in a machine-readable format
    that can be scanned by smartphones and other devices.

Dependencies:
    - qrcode  (pip install qrcode[pil])
    - Pillow  (installed automatically with qrcode[pil])

Usage:
    python qr_generator.py
"""

import os
import sys

import qrcode
from qrcode.constants import ERROR_CORRECT_H


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_OUTPUT_FILE = "qr_code.png"   # Default filename for the saved image
QR_VERSION         = 1                # Version 1–40; None lets the library auto-select
BOX_SIZE           = 10               # Pixel size of each individual "box" in the QR grid
BORDER             = 4                # Minimum quiet-zone thickness (in boxes) — spec requires ≥ 4
FILL_COLOR         = "black"          # Foreground (module) color
BACK_COLOR         = "white"          # Background color


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def get_url_from_user() -> str:
    """
    Prompt the user to enter a URL and return the validated string.

    Returns:
        str: A non-empty URL string provided by the user.

    Raises:
        SystemExit: If the user provides an empty string or only whitespace.
    """
    url = input("Enter the URL to encode as a QR code: ").strip()

    if not url:
        print("Error: No URL was entered. Please run the program again and provide a valid URL.")
        sys.exit(1)

    return url


def generate_qr_code(url: str, output_file: str = DEFAULT_OUTPUT_FILE) -> qrcode.image.base.BaseImage:
    """
    Generate a QR code image for the given URL and save it to disk.

    Parameters:
        url         (str): The URL or data string to encode.
        output_file (str): The filename (including extension) where the image will be saved.

    Returns:
        qrcode.image.base.BaseImage: The generated QR code image object.
    """
    # -----------------------------------------------------------------
    # Configure the QR code encoder
    #   error_correction = ERROR_CORRECT_H allows up to 30 % of the
    #   code to be damaged/obscured while still being decodable.
    # -----------------------------------------------------------------
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=BORDER,
    )

    # Add the URL data to the QR code
    qr.add_data(url)

    # Optimize the QR code matrix (find best version/data type)
    qr.make(fit=True)

    # Render the QR code as a PIL image
    img = qr.make_image(fill_color=FILL_COLOR, back_color=BACK_COLOR)

    # Save the image to the specified output file
    img.save(output_file)

    return img


def display_summary(url: str, output_file: str) -> None:
    """
    Print a summary of the generated QR code to the console.

    Parameters:
        url         (str): The URL that was encoded.
        output_file (str): The path where the image was saved.
    """
    abs_path = os.path.abspath(output_file)
    file_size_kb = os.path.getsize(abs_path) / 1024

    print("\n" + "=" * 55)
    print("        Biox Systems — QR Code Generator")
    print("=" * 55)
    print(f"  URL Encoded : {url}")
    print(f"  Output File : {abs_path}")
    print(f"  File Size   : {file_size_kb:.2f} KB")
    print("=" * 55)
    print("  QR code successfully generated!")
    print("  Open the PNG file to view and scan your QR code.")
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Main function — orchestrates the QR code generation workflow:
        1. Collect a URL from the user.
        2. Generate the QR code image.
        3. Save the image and display a summary.
    """
    print("\nWelcome to the Biox Systems QR Code Generator")
    print("----------------------------------------------")

    # Step 1: Get the URL from the user
    url = get_url_from_user()

    # Step 2: Optionally allow a custom output filename
    custom_file = input(
        f"Enter output filename (press Enter to use '{DEFAULT_OUTPUT_FILE}'): "
    ).strip()
    output_file = custom_file if custom_file else DEFAULT_OUTPUT_FILE

    # Ensure the filename ends with a recognised image extension
    if not output_file.lower().endswith((".png", ".jpg", ".jpeg")):
        output_file += ".png"

    print(f"\nGenerating QR code for: {url}")

    # Step 3: Generate and save the QR code
    generate_qr_code(url, output_file)

    # Step 4: Display a confirmation summary
    display_summary(url, output_file)


# ---------------------------------------------------------------------------
# Script Guard — only run main() when executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
