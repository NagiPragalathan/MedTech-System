import pytesseract
from PIL import Image

# Path to the Tesseract executable (change this if it's installed in a different location)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    Extract text from an image.
    
    Args:
    - image_path (str): Path to the image file.
    
    Returns:
    - text (str): Extracted text from the image.
    """
    # Open the image file
    with Image.open(image_path) as img:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img)
    return text



# Example usage
image_path = 'example.jpg'
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)
