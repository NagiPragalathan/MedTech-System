from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import pytesseract
from PIL import Image
import io
from PyPDF2 import PdfReader
from hospital.models import Patient , PatientDocument



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@csrf_exempt
def upload_image_view(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        
        if is_valid_image(uploaded_file):        
            extracted_text = extract_text_from_image(uploaded_file)
        else:
            extracted_text = extract_text_from_pdf(uploaded_file)
        
        print("Extracted Text:")
        print(extracted_text)
        
        return HttpResponse(extracted_text)
    else:
        patient = Patient.objects.get(user=request.user)
        context = {'patient': patient}
        
        return render(request, 'OCR_Ai/get_file.html',context)

def is_valid_image(image):
    """
    Check if the uploaded file is a valid image.
    
    Args:
    - image: Uploaded file object.
    
    Returns:
    - valid (bool): True if the file is a valid image, False otherwise.
    """
    # Get the file extension
    file_extension = image.name.split('.')[-1].lower()
    
    # Check if the file extension corresponds to an image format
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if file_extension in valid_extensions:
        return True
    else:
        return False

def extract_text_from_image(image):
    """
    Extract text from an image.
    
    Args:
    - image: Image file object.
    
    Returns:
    - text (str): Extracted text from the image.
    """
    # Open the image file
    with Image.open(image) as img:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img)
    return text


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
    - pdf_file: PDF file object.
    
    Returns:
    - text (str): Extracted text from the PDF.
    """
    # Read the content of the PDF file
    pdf_content = pdf_file.read()
    
    # Create a PdfReader object
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    
    # Initialize an empty string to store the extracted text
    extracted_text = ""
    
    # Iterate through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page and append it to the extracted_text string
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    return extracted_text
    