pip install pytesseract pillow opencv-python
pip install pytesseract
pip install pillow
pip install opencv-python
apt-get install -y tesseract-ocr
pip install pytesseract

import pytesseract
from PIL import Image
import cv2
import os

def preprocess_image(image_path):
    """Preprocess the image for better OCR accuracy."""
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        exit()

    image = cv2.imread(image_path)
    if image is None:
        print("Error: Failed to load the image. Please check the file path or format.")
        exit()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image_path):
    """Extract text from the image."""
    processed_image = preprocess_image(image_path)
    return pytesseract.image_to_string(processed_image)

if __name__ == "__main__":
    # Install Tesseract in Colab (uncomment if not already installed)
    # !apt-get install -y tesseract-ocr
    # !pip install pytesseract

    # Path to the uploaded image
    image_path = "sample_data/image_path.webp"  # Replace with the correct file name

    # Extract and display text
    extracted_text = extract_text(image_path)
    print("Extracted Text:")
    print(extracted_text)

import re

# Raw OCR output (example data for demonstration)
ocr_text = extracted_text

def preprocess_text(ocr_text):
    """Extract and structure data from the OCR output."""
    # Clean up the text
    cleaned_text = re.sub(r'\s+', ' ', ocr_text)  # Remove excessive whitespace
    cleaned_text = re.sub(r'[^\w\s:,+\-]', '', cleaned_text)  # Remove unwanted characters

    # Extract fields using regular expressions
    data = {}
    data['Name'] = re.search(r'Name\s?[:;,]?\s?([\w\s]+)', cleaned_text, re.IGNORECASE).group(1).strip()
    data['Date of Birth'] = re.search(r'Date of Birth\s?[:;,]?\s?([\w\-]+)', cleaned_text, re.IGNORECASE).group(1).strip()
    data['Gender'] = re.search(r'Sex\s?[:;,]?\s?(\w+)', cleaned_text, re.IGNORECASE).group(1).strip()
    data['Place of Birth'] = re.search(r'Place of Birth\s?[:;,]?\s?([\w\s]+)', cleaned_text, re.IGNORECASE).group(1).strip()
    data['Father\'s Name'] = re.search(r'Name of Father\s?[:;,]?\s?([\w\s]+)', cleaned_text, re.IGNORECASE).group(1).strip()
    data['Mother\'s Name'] = re.search(r'Name of Mother\s?[:;,]?\s?([\w\s]+)', cleaned_text, re.IGNORECASE).group(1).strip()

    # Match registration number (handle missing matches)
    reg_num_match = re.search(r'Registration Number\s?[:;,]?\s?[+]?([\d]+)', cleaned_text, re.IGNORECASE)
    data['Registration Number'] = reg_num_match.group(1).strip() if reg_num_match else "Not Available"

    # Match date of registration (handle missing matches)
    reg_date_match = re.search(r'Date Of Registration\s?[:;,]?\s?([\w\-]+)', cleaned_text, re.IGNORECASE)
    data['Date of Registration'] = reg_date_match.group(1).strip() if reg_date_match else "Not Available"

    # Optional: Address if present
    address_match = re.search(r'Address at the time of Birth\s?[:;,]?\s?([\w\s,]+)', cleaned_text, re.IGNORECASE)
    data['Address'] = address_match.group(1).strip() if address_match else "Not Available"

    return data

# Extract and print the data
extracted_data = preprocess_text(ocr_text)

print("Extracted Data:")
for key, value in extracted_data.items():
    print(f"{key}: {value}")

# Ask the user for confirmation or changes
print("\nIs the above information correct? If there are any changes, please specify them.")
user_response = input("Enter your changes in the format 'Field: Corrected Value', or type 'yes' to confirm: ")

while user_response.lower() != 'yes':
    # Parse the user's input for updates
    try:
        field, corrected_value = user_response.split(":", 1)
        field = field.strip()
        corrected_value = corrected_value.strip()

        if field in extracted_data:
            extracted_data[field] = corrected_value
            print(f"{field} updated to: {corrected_value}")
        else:
            print(f"Field '{field}' not found. Please check the field name.")

    except ValueError:
        print("Invalid format. Please use the format 'Field: Corrected Value'.")

    # Ask for more updates or confirmation
    print("\nUpdated Data:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")

    user_response = input("Enter your changes in the format 'Field: Corrected Value', or type 'yes' to confirm: ")

print("\nFinal Confirmed Data:")
for key, value in extracted_data.items():
    print(f"{key}: {value}")

print("Data saved successfully!")
